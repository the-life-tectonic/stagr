<!DOCTYPE html>
<@
from datetime import datetime
suite = request.suite
now = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
@>
<@# display the time the report was generated '@>
<!-- report generated at %(now)s -->
<html>
<head>
	<link href="http://fonts.googleapis.com/css?family=Quicksand:700|Droid+Sans+Mono|Chivo" rel="stylesheet" type="text/css">
	<link href="style/style.css" rel="stylesheet" type="text/css" />
	<title>%(suite.name)s</title>
	<script type="text/javascript">
//<![CDATA[
function toggle_display(class_name,a)
{
	var f = new Function( "node", "toggle(node,'"+class_name+"');" );
	traverse_children(document.body,f);
	var msg=''
	if( a.innerHTML.indexOf('hide')!=-1 )
	{
		msg=a.innerHTML.replace('hide','show');
	}
	else
	{
		msg=a.innerHTML.replace('show','hide');
	}
	a.innerHTML=msg;
}

function toggle(node,class_name)
{
	if ( node.className.split(' ').indexOf(class_name) != -1 )
	{
		if (node.style.display.toLowerCase()=="none")
		{
			node.style.display="";
		}
		else
		{
			node.style.display="none";
		}
	}
}

function traverse_children(node,f)
{
	if(node.children)
	{
		var kids=node.children;
		for (var i=0; i<kids.length; i++)
		{
			var kid=kids[i];
			f(kid);
			if( kid.children && kid.children.length>0 )
			{
				traverse_children(kid,f);
			}
		}	
	}
}

function formsubmit(button)
{
	var f=button.form;
	f.action=button.name;
	f.submit();
}

function toggle_all(checkbox,name)
{
	var f=checkbox.form;
	var elms=f.elements;
	for( var i=0; i<elms.length; i++)
	{
		e=elms[i]
		if(e.name==name)
		{
			e.checked=checkbox.checked
		}
	}
}
//]]>
	</script>
</head>
<body>
	<h1>%(suite.name)s</h1>
	<pre class="suite_description">
%(request.suite.description)s
	</pre>
	<h2>Models</h2>
<form action="movie.html">
<table class="model_table">
<tr>
	<th style="text-align: left; padding-left: 5px; padding-right: 5px;"><input type="checkbox" onclick="toggle_all(this,'model')"></th>
	<th>Model<br/><a href="#" onclick="toggle_display('model_description',this);return false;" style="font-size: smaller">hide description</a></th>
<@for diff in suite.par_diff : @>
	<th>%(diff.section)s<br/>%(diff.key)s</th>
<@ @>
</tr>

<@
model_number=0
styles={ bool: 'text-align: center;',str: 'text-align: left', int: 'text-align: right;', float: 'text-align: right'}
col_span=len(suite.par_diff)+2
@>
<@#Loop over the models@>
<@for model in suite.models : @>
<tr>
	<td style="text-align: left"><input type="checkbox" name="model" value="%(model.name)s"></td>
	<td style="text-align: left"><a href="%(model.name)s">%(model.name)s</a><pre class="model_description foo">%(model.description)s</pre></td>
<@for diff in suite.par_diff : 
	value=diff['values'][model_number]
	style=styles[type(value)]
@>
	<td class="mono" style="%(style)s">%(value)s</td>
<@ @>
</tr>
<@model_number=model_number+1@>
<@ @>

<@
fields=sorted(set(suite.fields)&set(request.fields))
@>
<tr><td colspan="%(col_span)d" style="text-align: left; border-bottom: none; padding-top: 10px;">
	<input type="button" name="movie.html" value="field plots" onclick="formsubmit(this)">
<@
import stagyy.field
for f in fields:
	field_name=stagyy.field.fields[f].name
@>
	<input type="checkbox" name="field" value="%(f)s"> %(field_name)s &nbsp;&nbsp;&nbsp;
<@ @>
</td></tr>
<tr><td colspan="%(col_span)d" style="text-align: left; border-bottom: none; padding-top: 10px;">
	<input type="button" name="modeltime.html" value="model time plots" onclick="formsubmit(this)">
</td></tr>

</table>
</form>

</body>
</html>
