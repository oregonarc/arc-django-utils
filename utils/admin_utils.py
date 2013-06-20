import json

from django.http import HttpResponse


def export_as_json(modeladmin, request, queryset):
    """
    Dumps the selected entries as a JSON list.

    """
    
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='application/json')
    response['Content-Disposition'] = 'attachment; filename=%s.json' % unicode(opts).replace('.', '_')

    out = []
    for q in queryset:
        fields = q._meta.fields
        row = {}
        for field in fields:
            if not getattr(q,field.name):
                if field.blank:
                    value = ""
                if field.null:
                    value = None
            else:
                value = field.value_to_string(q)
            row.update({field.name:value})
        out.append(row)

    out = json.dumps(out)
    response.write(out)
    return response


def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    
    To add admin model properties to CSV files first add the properties to the appropriate model.
    Then in the ModelAdmin class add a list name "csv_extras" containing a list of property you want to show up in the CSV file.
    The will be prepended to the columns of the CSV file.  This only works with properties, not methods.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
        
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
   
    # Check for CSV extra fields specified in modeladmin
    try:
        csv_extras = modeladmin.csv_extras
        field_names = csv_extras+field_names
    except:
        pass    
    
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([ getattr(obj, field) or "" for field in field_names])
    return response