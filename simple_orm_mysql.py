#coding:utf-8
class FieldError():
   def __init__(self, arg):
      self.args = arg

class Utils(object):
   def join_where(self,kwargs): 
        str_list = []
        index = 0
        for i in kwargs.iteritems():
            if not index == len(kwargs):
                str = "%s=%s"%(i[0],i[1])
                str_list.append(str)
                index +=1
        where_sql = ' and '.join(str_list)        
        return where_sql
    
        

class Model(Utils):
    def __init__(self, rid=0, **kwargs):
        self.table_name = self.__class__.__name__.lower()
        for name in self.field_names:
            field = getattr(self.__class__, name.replace("`", ""))
            setattr(self, name.replace("`", ""), field.default)
        for key, value in kwargs.items():
            setattr(self, key.replace("`", ""), value)
#        self.debug()

    def debug(self):
        for name in dir(self.__class__):
            print name,'-------',getattr(self.__class__,name)

    @property
    def field_names(self):
        names = []
        for name in dir(self.__class__):
            var = getattr(self.__class__, name.replace("`", ""))
            if isinstance(var, Field):                
                names.append("`%s`"%name)
        return names

    @property
    def field_values(self):
        values = []
        for name in self.field_names:
            value = getattr(self, name.replace("`", ""))
            if isinstance(value, Model):
                value = value.id
            if isinstance(value, str):
                value = value.replace("'", "''")
                try:
                    value = value.decode("gbk")
                except Exception, e:
                    pass
                try:
                    value = value.decode("utf8")
                except Exception, e:
                    pass
            values.append("'%s'" % value)
        return values

    def get_cursor(self):
        return None

    def insert(self):
        cu = self.get_cursor()

        field_names_sql = ", ".join(self.field_names)
        field_values_sql = ", ".join(self.field_values)

        sql = "insert into '%s'(%s) values(%s)" % (self.table_name, field_names_sql, field_values_sql)
        print sql

    def update(self):
        cu = get_cursor()

        name_value = []
        for name, value in zip(self.field_names, self.field_values):
            name_value.append("%s=%s" % (name, value))
        name_value_sql = ", ".join(name_value)

        sql = "update `%s` set %s where id = %d" % (self.table_name, name_value_sql, self.id)
        print sql

    def save(self):
        self.insert()

    def delete(self):
        cu = get_cursor()
        sql = "delete from `%s` where id = %d" % (self.table_name, self.id)
        print sql

    def get(self, **kwargs):
        where_sql = self.join_where(kwargs)
        sql = "select * from %s where %s"%(self.table_name,where_sql)
        print sql

class Field(object):
    field_type = ""
    field_level = 0
    default = ""

    def field_sql(self, field_name):
        return '"%s" %s' % (field_name, self.field_type)

class CharField(Field):
    def __init__(self, max_length=255, default=""):
        self.field_type = "varchar(%d)" % max_length
        self.default = default
        self.max_length = max_length

def ValidField(max_length):
    if max_length > 255:
        raise FieldError('max_lenth lt 255')
