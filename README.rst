Product Match
#############

A test web scraper and NLP classifier using BeautifulSoup and NLTK.

Example Classifier Test Output
==============================

Classifier for categories 1 level deep:
---------------------------------------

>python nlp.py -c 1
Loading data from directory: ./data
Classifying product descriptions up to a product category hierarchy depth of 1.
9886 Data Samples.
Generating features...
Training Classifier...
Testing Accuracy...
Most Informative Features
          contains(item) = False          Beauty : Jewelr =   4171.1 : 1.0
           contains(tax) = True           Beauty : Jewelr =   3562.5 : 1.0
          contains(card) = True           Beauty : Jewelr =   3562.5 : 1.0
       contains(minimum) = True           Beauty : Jewelr =   3562.5 : 1.0
        contains(veneer) = True           furnit : Jewelr =   3529.9 : 1.0
            contains(42) = True           furnit : Jewelr =   3529.9 : 1.0
       contains(consist) = True           Kitche : Jewelr =   3355.6 : 1.0
         contains(bevel) = True           Kitche : Jewelr =   3355.6 : 1.0
         contains(stain) = True           Kitche : Jewelr =   3355.6 : 1.0
          contains(area) = True           Kitche : Jewelr =   3355.6 : 1.0
          contains(feet) = True           Kitche : Jewelr =   3355.6 : 1.0
          contains(fair) = True           Holida : Jewelr =   3299.2 : 1.0
       contains(artisan) = True           Holida : Jewelr =   3299.2 : 1.0
         contains(price) = True           Holida : Jewelr =   3299.2 : 1.0
          contains(valu) = True           Beauty : Jewelr =   2345.1 : 1.0
            contains(72) = True           Shower : Jewelr =   2284.1 : 1.0
        contains(shower) = True           Shower : Jewelr =   2284.1 : 1.0
      contains(checkout) = True           Beauty : Jewelr =   2137.5 : 1.0
          contains(home) = True           Kitche : Jewelr =   2013.4 : 1.0
      contains(composit) = True           Kitche : Jewelr =   2013.4 : 1.0
        contains(origin) = True           Kitche : Jewelr =   2013.4 : 1.0
          contains(curl) = True           Kitche : Jewelr =   2013.4 : 1.0
         contains(charg) = True           Beauty : Jewelr =   1634.2 : 1.0
       contains(polyest) = True           Shower : Jewelr =   1631.5 : 1.0
        contains(import) = True           Shower : Jewelr =   1631.5 : 1.0
Accuracy: 0.977755308392
A few examples:
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: for the home | Prediction: for the home
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: for the home | Prediction: for the home
Actual: for the home | Prediction: for the home
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: for the home | Prediction: for the home
Actual: Bed & Bath | Prediction: Bed & Bath
Actual: Bed & Bath | Prediction: Bed & Bath
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: Jewelry & Watches
Actual: Bed & Bath | Prediction: Bed & Bath

Classifier for categories 2 levels deep
---------------------------------------

>python nlp.py -c 2
Loading data from directory: ./data
Classifying product descriptions up to a product category hierarchy depth of 2.
9886 Data Samples.
Generating features...
Training Classifier...
Testing Accuracy...
Most Informative Features
           contains(tax) = True           See Al : FINE J =   3886.8 : 1.0
          contains(card) = True           See Al : FINE J =   3886.8 : 1.0
       contains(minimum) = True           See Al : FINE J =   3886.8 : 1.0
      contains(warranti) = True           Watche : FINE J =   3768.0 : 1.0
          contains(dial) = True           Watche : FINE J =   3539.6 : 1.0
          contains(valu) = True           Skin C : FINE J =   3350.5 : 1.0
       contains(consist) = True           Kitche : FINE J =   3108.3 : 1.0
          contains(area) = True           Kitche : FINE J =   3108.3 : 1.0
         contains(price) = True           Holida : FINE J =   3056.0 : 1.0
       contains(artisan) = True           Holida : FINE J =   3056.0 : 1.0
         contains(clock) = True           Watche : FINE J =   2854.5 : 1.0
         contains(numer) = True           Watche : FINE J =   2854.5 : 1.0
         contains(month) = True           Makeup : FINE J =   2397.8 : 1.0
          contains(item) = False          GIFTS  : FINE J =   2286.3 : 1.0
        contains(import) = True           Slipco : FINE J =   2265.3 : 1.0
       contains(polyest) = True           Shower : FINE J =   2115.7 : 1.0
        contains(shower) = True           Shower : FINE J =   2115.7 : 1.0
          contains(help) = True           Makeup : FINE J =   2078.1 : 1.0
           contains(tip) = True           Skin C : FINE J =   2058.7 : 1.0
          contains(safe) = True           Casual : FINE J =   2028.9 : 1.0
          contains(tuck) = True           Slipco : FINE J =   2009.2 : 1.0
          contains(home) = True           Quilts : FINE J =   1961.8 : 1.0
        contains(sensit) = True           GIFTS  : FINE J =   1951.7 : 1.0
          contains(case) = True           Watche : FINE J =   1941.1 : 1.0
        contains(origin) = True           Kitche : FINE J =   1865.0 : 1.0
Accuracy: 0.864509605662
A few examples:
Actual: Home Decor | Prediction: Home Decor
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: Jewelry & Watches | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: Jewelry & Watches
Actual: Home Decor | Prediction: Home Decor
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: Bedding Basics | Prediction: Bedding Basics
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: Home Decor | Prediction: Home Decor
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: Jewelry & Watches
Actual: Jewelry & Watches | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY
Actual: FINE JEWELRY | Prediction: FINE JEWELRY

Classifier for categories 3 levels deep:
---------------------------------------

>python nlp.py -c 3
Loading data from directory: ./data
Classifying product descriptions up to a product category hierarchy depth of 3.
9886 Data Samples.
Generating features...
Training Classifier...
Testing Accuracy...
Most Informative Features
          contains(item) = False          Collec : Earrin =   1339.8 : 1.0
           contains(tax) = True           SHOP A : Earrin =   1308.8 : 1.0
          contains(card) = True           SHOP A : Earrin =   1308.8 : 1.0
         contains(charg) = True           SHOP A : Earrin =   1308.8 : 1.0
       contains(minimum) = True           SHOP A : Earrin =   1308.8 : 1.0
         contains(clock) = True           Clocks : Neckla =   1292.9 : 1.0
        contains(import) = True           Slipco : Earrin =   1291.9 : 1.0
      contains(bracelet) = True           Bracel : Neckla =   1269.4 : 1.0
         contains(limit) = True           Watche : Neckla =   1252.4 : 1.0
        contains(cotton) = True           Bath R : Neckla =   1197.7 : 1.0
          contains(heat) = True           Hair C : Earrin =   1163.4 : 1.0
       contains(artisan) = True           Gifts  : Earrin =   1141.0 : 1.0
      contains(ornament) = True           Holida : Neckla =   1124.0 : 1.0
          contains(half) = True           Gifts  : Earrin =   1070.8 : 1.0
        contains(receiv) = True           Gifts  : Neckla =   1052.3 : 1.0
        contains(origin) = True           Kitche : Earrin =   1051.3 : 1.0
       contains(comfort) = True           Kitche : Earrin =   1051.3 : 1.0
           contains(100) = True           Kitche : Earrin =   1051.3 : 1.0
           contains(...) = True           Kitche : Earrin =   1051.3 : 1.0
           contains(use) = True           Skin C : Neckla =   1039.0 : 1.0
       contains(consist) = True           Kitche : Neckla =   1033.1 : 1.0
          contains(slip) = True           Kitche : Neckla =   1033.1 : 1.0
         contains(brush) = True           Skin C : Neckla =   1012.7 : 1.0
         contains(candl) = True           Candle : Neckla =    948.8 : 1.0
            contains(aa) = True           Clocks : Earrin =    847.0 : 1.0
Accuracy: 0.866531850354
A few examples:
Actual: Rings | Prediction: Rings
Actual: Shower Curtains & Accessories | Prediction: Shower Curtains & Accessories
Actual: Earrings | Prediction: Earrings
Actual: Earrings | Prediction: Jewelry & Watches
Actual: Bath Towels | Prediction: Bath Towels
Actual: Jewelry & Watches | Prediction: Earrings
Actual: Rings | Prediction: Rings
Actual: Earrings | Prediction: Earrings
Actual: Necklaces | Prediction: Necklaces
Actual: Bracelets | Prediction: Bracelets
Actual: Bath Towels | Prediction: Bath Towels
Actual: Earrings | Prediction: Earrings
Actual: Necklaces | Prediction: Necklaces
Actual: Candles & Home Fragrance | Prediction: Candles & Home Fragrance
Actual: Bracelets | Prediction: Bracelets
Actual: Necklaces | Prediction: Necklaces
Actual: Earrings | Prediction: Earrings
Actual: Earrings | Prediction: Earrings
Actual: Bowls & Vases | Prediction: Collections
Actual: Hair Care | Prediction: Hair Care
