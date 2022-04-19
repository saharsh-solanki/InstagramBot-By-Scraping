# InstagramBot-By-Scraping
## InProgress 

## You Can Start Using Bot Now But 

## How Does this work ? 

## Create Intance of class 

To create Cookie File 

```
bot = InitiateBot("username","password")
```

## Username And Password Is Option But How Can it work without login . Basicaly i am creating a cookie file once it is created we don't need to again perform login  

If Cookie File Already Exists
```
bot = InitiateBot()
```


## Perform Login And create Cookie file 

```
bot = InitiateBot("username","password")
bot.PerformLogin()
```


##  You Can directly call this method get and set the cookie for the current instance 

### Without PerformLogin()

```
bot = InitiateBot()
bot.setAndCheckCookie()
```

### With login 

```
bot = InitiateBot("username","password")
bot.PerformLogin()
bot.setAndCheckCookie()
```

## And Finaly We have Our Main Function 

```
bot.FollowFollowerOfAPersonByUsername("simran.mahawar05")
```