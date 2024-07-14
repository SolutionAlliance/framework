# flask 企业级基础框架
`celery` `flask` `Docker`  `redis` `mysql` `Restful-Api`

- [开发文档](/docs/README.md)
- [业务目录清单](/app/README.md)
- [`程序发版日志-每次发版需要更新`](/CHANGELOG.md)

# 项目结构
```md
├── CHANGELOG.md
├── Dockerfile
├── Procfile
├── README.md
├── app
│   ├── README.md
│   ├── __init__.py                 # flask app 核心
│   ├── common                      # 公共方法或者类
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── email.py
│   │   ├── logger.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   ├── security.py
│   │   ├── snowflakeAlgorithm.py
│   │   └── utils.py
│   ├── example
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── schemas
│   │   │   ├── README.md
│   │   │   ├── __init__.py
│   │   │   └── example_schemas.py
│   │   ├── utils
│   │   │   └── __init__.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── export_view.py
│   └── tasks                       # celery 后台任务
│       ├── __init__.py
│       └── example.py
├── boot.sh
├── config.py                       # 程序环境配置
├── docs
│   └── README.md
├── manager.py                      # 程序启动入口
├── migrations                      # 数据库版本控制
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 0abc80edb8db_v1_0_3.py
│       ├── 9cca611b2e3c_v1_0_1.py
│       ├── a3af097384c6_v1_0_2.py
│       ├── db90f452c4f7_v1_0_0.py
│       └── eb6077695684_v1_0_4.py
├── requirements                    # python 环境依赖
│   ├── common.txt
│   ├── dev.txt
│   └── prod.txt
├── requirements.txt
└── tests
    └── __init__.py
```