# Flask Marshmallow schema
- [Flask Marshmallow基本使用](https://blog.csdn.net/yutu75/article/details/110457378)

# schema常用属性数据类型
| 类型 | 描述
| -------- | -------------- |
| fields.Dict(keys, type]] = None, values, …)	 | 字典类型，常用于接收json类型数据
| fields.List(cls_or_instance, type], **kwargs) | 	列表类型，常用于接收数组数据
| fields.Tuple(tuple_fields, *args, **kwargs)	 | 元组类型
| fields.String(*, default, missing, data_key, …)	 | 字符串类型
| fields.UUID(*, default, missing, data_key, …)	 | UUID格式类型的字符串
| fields.Number(*, as_string, **kwargs)	 | 数值基本类型
| fields.Integer(*, strict, **kwargs)	 | 整型
| fields.Decimal(places, rounding, *, allow_nan, …)	 | 数值型
| fields.Boolean(*, truthy, falsy, **kwargs)	 | 布尔型
| fields.Float(*, allow_nan, as_string, **kwargs)	 | 浮点数类型
| fields.DateTime(format, **kwargs)	 | 日期时间类型
| fields.Time(format, **kwargs)	 | 时间类型
| fields.Date(format, **kwargs) | 	日期类型
| fields.Url(*, relative, schemes, Set[str]]] = None, …)	 | url网址字符串类型
| fields.Email(*args, **kwargs)	 | 邮箱字符串类型
| fields.IP(*args[, exploded])	 | IP地址字符串类型
| fields.IPv4(*args[, exploded])	 | IPv4地址字符串类型
| fields.IPv6(*args[, exploded])	 | IPv6地址字符串类型
| fields.Method(serialize, deserialize, **kwargs)	 | 基于Schema类方法返回值的字段
| fields.Function(serialize, Any], Callable[[Any, …)	 | 基于函数返回值得字段
| fields.Nested(nested, type, str, Callable[[], …)	 | 外键类型

# Schema数据类型的常用通用属性
| 属性名 | 描述
| -------- | -------------- |
| default	 | 序列化阶段中设置字段的默认值
| missing	 | 反序列化阶段中设置字段的默认值
| validate	 | 反序列化阶段调用的内置数据验证器或者内置验证集合
| required	 | 设置当前字段的必填字段
| allow_none	 | 是否允许为空
| load_only	 | 是否在反序列化阶段才使用到当前字段
| dump_omly	 | 是否在序列化阶段才使用到当前字段
| error_messages	 | 字典类型，可以用来替代默认的字段异常提示语，格式：error_messages={“required”: “用户名为必填项。”}