<@
suite=request.suite
desc=repr(suite.description)
@>

var suite=new Object();
suite.models=new Object();
suite.name='%(suite.name)s';
suite.description=%(desc)s;
suite.max_last_timestep=%(suite.max_last_timestep)d;
suite.min_last_timestep=%(suite.min_last_timestep)d;
suite.models=[];
suite.model_map={};
<@for model in suite.models:
	desc=repr(model.description)
@>
// %(model.name)s
model=new Object()
model.name='%(model.name)s';
model.description=%(desc)s;
model.last_timestep=%(model.last_timestep)s;
model.total_timesteps=%(model.total_timesteps)s;
model.plot_file_prefix='%(model.plot_file_prefix)s'
model.frames='%(model.frames)s';
// Add the model to the suite
suite.models[suite.models.length]=model
suite.model_map['%(model.name)s']=model
<@ @>

stagyy_fields={}
<@
import stagyy.field as sf
for field in sf.fields.values():
	scalar=str(field.scalar).lower()
@>
field=new Object();
field.name='%(field.name)s';
field.prefix='%(field.prefix)s';
field.scalar=%(scalar)s;
stagyy_fields['%(field.prefix)s']=field
<@ @>
