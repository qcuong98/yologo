# YOLOGO
Brand Logo Detection Using YOLOv3

# Dataset

  - Source: [Flickr Logos 27](http://image.ntua.gr/iva/datasets/flickr_logos/)

  - Consists of 27 brands: Adidas, Apple,
    BMW, Citroen, Coca Cola, DHL, Fedex, Ferrari, Ford, Google,
    Heineken, HP, McDonalds, Mini, Nbc, Nike, Pepsi, Porsche, Puma, Red
    Bull, Sprite, Starbucks, Intel, Texaco, Unisef, Vodafone, and Yahoo
    
# API

  - Construct a RESTful API using Flask library for Python 3 for 2 weights: YOLOv3 (default weight)
    and YOLOGO (brand logo weight)

  - Protocol: POST

  - YOLOv3 address: `[HOST]:8080/model_1`
  
  - YOLOGO address: `[HOST]:8080/model_2`

  - Structure: multipart-form with field **file** to save the request image

  - Return a JSON file, if the image is valid then return class, bounding box, and confident of objects

  - Example:

<!-- end list -->

``` json
Input: curl -F file=@dog.jpg [HOST]:8080/model_1
Output:
{
  "code":0,
  "description":"OK",
  "objects":[
    {"bbox":{"h":328,"w":179,"x":134,"y":214}, "class":"dog","conf":0.9993382096290588},
    {"bbox":{"h":324,"w":490,"x":99,"y":124}, "class":"bicycle","conf":0.993359386920929},
    {"bbox":{"h":87,"w":208,"x":476,"y":81},"class":"truck","conf":0.9153257608413696}
  ]
}
```

![dog.jpg](dog.jpg?raw=true "dog.jpg")

# Website

UNMAINTAINED
