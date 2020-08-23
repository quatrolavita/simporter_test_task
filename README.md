###### Simporter Test Task 

This application requires two API methods `/api/info` and `/api/timeline`

`/api/info` 
This API method returns JSON with possible filtering (list of attributes and list of values for each attribute)
Like this:
``` json
{
  "asin": [<list of values>], 
  "brand": [<list of values>], 
  "source": [<list of values>], 
  "stars": [<list of values>]
}
```

`/api/timeline/?<params>`

This API method returns JSON with timeline information according to input parameters

Like this:

```
{“timeline”: 
[{
“date”: “2019-01-01”, 
"value": 10}, 
... 
] }

```

###### HOW TO START?

1. Clone git repo 

2. Install docker [tutorial](https://docs.docker.com/engine/install/ubuntu/)
3. `sudo docker-compose build app`
4. `sudo docker-compose up`
5.  Than you can follow `http://localhost:5000/api/info` or `http://localhost:5000/api/timeline?<params>`

If you want to restart app just enter commands below:

```
sudo docker-compose down
sudo docker-compose up
```

###### HOW TO TEST?

1. Clone git repo 

2. Install docker [tutorial](https://docs.docker.com/engine/install/ubuntu/)
3. `sudo docker-compose build app`
4. `sudo docker-compose run app sh -c "python manage.py test --coverage"`





