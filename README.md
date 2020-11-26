# python-flask-docker
Итоговый проект (пример) курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy, catboost
API: flask
Данные: с archive - https://archive.ics.uci.edu/ml/datasets/Early+stage+diabetes+risk+prediction+dataset

Задача: предсказать по результатам медицинского опроса вероятность наличия ранней стадии диабета (поле class). Бинарная классификация

Используемые признаки:

- Age (number)
- Gender (categorical)
- Polyuria (bool)
- Polydipsia (bool)
- sudden weight loss (bool)
- weakness (bool)
- Polyphagia (bool)
- Genital thrush (bool)
- visual blurring (bool)
- Itching (bool)
- Irritability	
- delayed healing (bool)
- partial paresis (bool)
- muscle stiffness (bool)
- Alopecia (bool)
- Obesity (bool)

Преобразования признаков: no

Модель: CatBoostClassifier

### for Windows
### Клонируем ветку репозитория и создаем образ
```
$ git clone --depth 1 -b final-project https://github.com/AlexanderKonstantinov/business_ml.git
$ cd business_ml\app
$ docker build -t diabetes_risk .
```

### Запускаем контейнер
```
$ docker run -d -p 8180:8180 -p 8181:8181 diabetes_risk
```

### Переходим на localhost:8181