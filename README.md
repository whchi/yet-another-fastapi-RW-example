# main concept
```shell
app
├── api                       - api related stuff
│   ├── contexts              - bounded contexts, add your context here
│   │   └── example           - domain name
│   │       ├── domain        - domain models, include exceptions, interfaces and pydanic models
│   │       ├── gateway       - interface adapter, includes presenter, repository, service...etc
│   │       ├── router.py     - router of this domain
│   │       └── usecase       - biz logic
│   ├── middlewares           - custom route middlewares
│   └── router.py             - router of whole app
├── core                      - core part of app
├── exceptions                - global custom exception handlers and definitions
├── models                    - orm models using sqlmodel
└── main.py                   - entrypoint
```
# references
* [https://github.com/Flaiers/fastapi-clean-architecture](https://github.com/Flaiers/fastapi-clean-architecture)
* [https://github.com/NEONKID/fastapi-ddd-example](https://github.com/NEONKID/fastapi-ddd-example)
* [https://github.com/iktakahiro/dddpy](https://github.com/iktakahiro/dddpy)
* [https://github.com/art049/fastapi-odmantic-realworld-example](https://github.com/art049/fastapi-odmantic-realworld-example)
* [https://github.com/nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)
