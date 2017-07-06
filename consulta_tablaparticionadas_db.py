



######  Consultar a tablas particionadas en bd con sus diferentes nombres#########
### tiws_tasacion_20170601####
### tiws_tasacion_20170602####
### tiws_tasacion_20170603####
### tiws_tasacion_20170604####
## Mejora el perfomance en un 70% ###
##### Permite sobreescribir y heredar la clase Padre #####


#### Modelos ###
def create_model(table):
    class MyClassMetaclass(ModelBase):
        def __new__(cls, *args, **kwargs):
            return Tasacion.base.ModelBase.__new__(cls, *args, **kwargs)
    class MyClass(Tasacion):
        __metaclass__ = MyClassMetaclass
        class Meta:
            db_table = table
    return MyClass

class Tasacion(models.Model):
    Secuenciaproceso = models.BigIntegerField(primary_key=True,db_column="tasa_secuenciaproceso")
    Secuenciaregistro = models.BigIntegerField(db_column="tasa_secuenciaregistro")
    Secuenciareproceso = models.BigIntegerField(blank=True, null=True,db_column="tasa_secuenciareproceso")
    Fechahora = models.DateTimeField(db_column="tasa_fechahora")
    Numeroorigen = models.CharField(max_length=20,db_column="tasa_numeroorigen")
    Nuor_pais = models.ForeignKey(Paises, null=True,db_column='tasa_nuor_pais',related_name='+')
    Match_hora = models.CharField(max_length=2, blank=True, null=True,db_column="tasa_match_hora")
    class Meta:
        managed = False
        abstract = True
        db_table = 'tiws_tasacion'
        unique_together = (('Secuenciaproceso', 'Secuenciaregistro', 'Nuor_pais'),)



#### View ###
from datetime import datetime, timedelta
from re import sub
def get_query(request):
    start_date = get_parser_date(request.GET.get('variable3'), None)
    end_date = get_parser_date(request.GET.get('variable4'), None)
    tasacion_list = []
    for item in daterange(start_date, end_date + ONEDAY):
        date_filter = datetime.strftime(item, '%Y-%m-%d')
        pref_sub = sub("[-]", '', date_filter.strip())
        table = 'tiws_tasacion_%s' % (pref_sub)
        newTasacion = create_model(table)
        tasacion_qs = newTasacion.objects.values(
                      'Secuenciaproceso','Secuenciareproceso'
                      ).filter(Match_fecha=item)
        tasacion_list += list(query)
    json_data = json.dumps(tasacion_list, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json')



def daterange(start_date, end_date):
    try:
        for item in range(int((end_date - start_date).days)):
            yield start_date + timedelta(item)
    except Exception as e:
        print("Function %s with error % e " % ('daterange', e))
