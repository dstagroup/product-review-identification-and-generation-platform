
const express = require("express"); 
const bodyParser = require("body-parser"); 
//app.js
const cors = require('cors');

const app = express();
app.use(bodyParser.json()); 
app.use(
  bodyParser.urlencoded({
    extended: true
  })
); 
app.use(cors());


app.all("*", function(request, response, next) {
  response.header("Access-Control-Allow-Origin", "*"); 
  response.header("Access-Control-Allow-Headers", "X-Requested-With");
  response.header(
    "Access-Control-Allow-Methods",
    "PUT,POST,GET,DELETE,OPTIONS"
  );
  response.header("X-Powered-By", " 3.2.1");
  response.header("Content-Type", "application/json;charset=utf-8");
  next();
});



app.get("/api/reviews", (request, response) => {
  
  request.statusCode = 200;
  console.log(request.query);
  var number_positive = Math.round(parseInt(request.query.num) / 2);
  var number_negative = parseInt(request.query.num) - number_positive;
  
  var asin = request.query.asin;


  const amazonScraper = require('amazon-buddy');
  (async () => {
    try {

      const product_by_asin = await amazonScraper.asin({ asin: asin });

      const reviews_negative = await amazonScraper.reviews({ asin: asin, number: number_negative, rating: [1, 2] });

      const reviews_positive = await amazonScraper.reviews({ asin: asin, number: number_positive, rating: [3, 5] });
      
      var brand = product_by_asin.result[0].product_information.brand;
      var title = product_by_asin.result[0].title;
      var description = product_by_asin.result[0].description;
      var feature_bullets = product_by_asin.result[0].feature_bullets;

      var list_negative = reviews_negative.result;
      var list_positive = reviews_positive.result;

      var negative_rv = [];
      var positive_rv = [];
      var n_item = {};
      var p_item = {};


      for (var i = 0; i < list_negative.length; i++) {

        n_item = {
          "title": list_negative[i].title,
          "review": list_negative[i].review,
          "rating": list_negative[i].rating
        }
        negative_rv.push(n_item);
      }


      for (var j = 0; j < list_positive.length; j++) {

        p_item = {
          "title": list_positive[j].title,
          "review": list_positive[j].review,
          "rating": list_positive[j].rating
        }

        positive_rv.push(p_item);
      }


      response.send({
        asin: asin,
        product_detail: {
          brand: brand,
          title: title,
          description: description,
          feature_bullets: feature_bullets
        },
        reviews: {
          positive_reviews: positive_rv,
          negative_reviews: negative_rv
        }
      });
      
    } catch (error) {

      response.send("error!");
    }
  })();
});

app.get("/api/reviews_all", (request, response) => {
  
  request.statusCode = 200;
  console.log(request.query);
  var asin = request.query.asin;

  const amazonScraper = require('amazon-buddy');
  (async () => {
    try {


      const product_by_asin = await amazonScraper.asin({ asin: asin });

      const reviews_negative = await amazonScraper.reviews({ asin: asin, number: 1000, rating: [1, 2] });

      const reviews_positive = await amazonScraper.reviews({ asin: asin, number: 1000, rating: [3, 5] });
      console.log(reviews_negative);
      
      var brand = product_by_asin.result[0].product_information.brand;
      var title = product_by_asin.result[0].title;
      var description = product_by_asin.result[0].description;
      var feature_bullets = product_by_asin.result[0].feature_bullets;
      var main_image = product_by_asin.result[0].main_image;

      var detail = {
        "brand": brand,
        "title": title,
        "description": description,
        "feature_bullets": feature_bullets,
        "main_image": main_image
      }


      var list_negative = reviews_negative.result;
      var list_positive = reviews_positive.result;

      var reviews = [];
     
      var n_item = {};
      var p_item = {};


      for (var i = 0; i < list_negative.length; i++) {

        n_item = {
          "title": list_negative[i].title,
          "review": list_negative[i].review,
          "rating": list_negative[i].rating
        }
        reviews.push(n_item);
      }


      for (var j = 0; j < list_positive.length; j++) {

        p_item = {
          "title": list_positive[j].title,
          "review": list_positive[j].review,
          "rating": list_positive[j].rating
        }

        reviews.push(p_item);
      }

      response.send({
        asin: asin,
        detail: detail,
        reviews: reviews
      });
      
    } catch (error) {

      response.send("error!");
    }
  })();
});


const hostname = "localhost";
const port = 8083;
const server = app.listen(port, hostname, () => {
  console.log(`我在运行了...`);
});
