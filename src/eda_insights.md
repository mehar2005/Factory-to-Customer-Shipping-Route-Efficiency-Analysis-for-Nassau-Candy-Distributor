# EDA Insights:
## Dataset shape :
|Number of variable|18
|Number of observations|10194

## Dataset description:
RangeIndex: 10194 entries, 0 to 10193
Data columns (total 18 columns):
|# |Column|Non-Null Count|Dtype|  
|0 |Row ID|10194 non-null|int64|  
|1 |Order ID|10194 non-null|object| 
|2 |Order Date|10194 non-null|object| 
|3 |Ship Date|10194 non-null|object| 
|4 |Ship Mode|10194 non-null|object| 
|5 |Customer ID|10194 non-null|int64|  
|6 |Country/Region|10194 non-null|object| 
|7 |City|10194 non-null|object| 
|8 |State/Province|10194 non-null|object| 
|9 |Postal Code|10194 non-null|object| 
|10|Division|10194 non-null|object| 
|11|Region|10194 non-null|object| 
|12|Product ID|10194 non-null|object| 
|13|Product Name|10194 non-null|object| 
|14|Sales|10194 non-null|float64|
|15|Units|10194 non-null|int64|  
|16|Gross Profit|10194 non-null|float64|
|17|Cost|10194 non-null|float64|
### dtypes: 
|float64|3|
|int64|3|
|object|12|
memory usage: 1.4+ MB

## Statistical summary:
Functions|Row ID|Customer ID|Sales|Units|Gross Profit|Cost|
|count |10194.000000  | 10194.000000  |10194.000000  |10194.000000  |10194.000000  |10194.000000 |
|mean  |  5097.500000 | 134468.961154 |    13.908537 |     3.791838 |     9.166451 |     4.742087|
|std   |  2942.898656 |  20231.483007 |    11.341020 |     2.228317 |     6.643740 |     5.061647|
|min   |     1.000000 | 100006.000000 |     1.250000 |     1.000000 |     0.250000 |     0.600000|
|25%   |  2549.250000 | 117212.000000 |     7.200000 |     2.000000 |     4.900000 |     2.400000|
|50%   |  5097.500000 | 133550.000000 |    10.800000 |     3.000000 |     7.470000 |     3.600000|
|75%   |  7645.750000 | 152051.000000 |    18.000000 |     5.000000 |    12.250000 |     5.700000|
|max   | 10194.000000 | 192314.000000 |   260.000000 |    14.000000 |   130.000000 |   130.000000|

## missing values per column:
|Row ID        | 0|
|Order ID      | 0|
|Order Date    | 0|
|Ship Date     | 0|
|Ship Mode     | 0|
|Customer ID   | 0|
|Country/Region| 0|
|City          | 0|
|State/Province| 0|
|Postal Code   | 0|
|Division      | 0|
|Region        | 0|
|Product ID    | 0|
|Product Name  | 0|
|Sales         | 0|
|Units         | 0|
|Gross Profit  | 0|
|Cost          | 0|
dtype: int64

### Duplicated values: 0

			Order Date
|Date format | "%d-%m-%Y"|
|Max date  |2025-12-31 00:00:00|
|Min date |2024-01-02 00:00:00|
|Unique dates| = 717|

### Orders per month:
|Order| Date|
|11   | 1474|
|12   | 1470|
|9    | 1399|
|10   |  843|
|5    |  758|
|6    |  725|
|8    |  722|
|7    |  718|
|3    |  711|
|4    |  670|
|1    |  404|
|2    |  300|

### Orders per year:
|2024  |  4181|
|2025  |  6013|

			Ship Date
|Date format | "%d-%m-%Y"|
|Max date | 2030-06-28 00:00:00|
|Min date | 2026-06-30 00:00:00|
|Unique dates| 1338|

### Shipments per month:
|8   |   388|
|7   |   415|
|9   |   689|
|1   |   706|
|11  |   709|
|10  |   712|
|12  |   745|
|2   |   797|
|4   |   880|
|6   |  1225|
|3   |  1357|
|5   |  1571|

### Shipments per year:
|2026  |   711|
|2027  |  2089|
|2028  |  2367|
|2029  |  2899|
|2030  |  2128|

> Columns containing outliers in the data:
1. Sales
2. Units
3. Gross Profit
4. Cost

### Unique values in categorical columns:
|Order ID| 8549|
|Order Date| 717|
|Ship Date|1338|
|Ship Mode| 4|
|Country/Region| 2|
|City| 542|
|State/Province| 59|
|Postal Code| 654|
|Division| 3|
|Region| 4|
|Product ID| 15|
|Product Name|15|

### Correlations:
1. Sales -> cost, gross profit(Very high) ; units(high)
2. Units -> sales, gross profit(high) ; cost(moderate)
3. Gross Profit -> sales(very high) ; units, cost(high)
4. Cost -> sales(very high) ; gross profit(high) ; units(moderate)

## Top 10 States by orders:
|California      |2001|
|New York        |1128|
|Texas           | 985|
|Pennsylvania    | 587|
|Washington      | 506|
|Illinois        | 492|
|Ohio            | 469|
|Florida         | 383|
|Michigan        | 255|
|North Carolina  | 249|

## Top 5 order dates by orders:
|2025-09-02   | 62|
|2025-12-01   | 57|
|2025-12-02   | 57|
|2025-12-09   | 54|
|2025-11-24   | 52|

## Top 5 ship dates by orders:
|2028-06-07  |  38|
|2030-05-29  |  35|
|2030-03-19  |  34|
|2030-05-14  |  32|
|2030-02-27  |  30|

## Ship Mode by orders:
|Standard Class  |  6120|
|Second Class    |  1979|
|First Class     |  1548|
|Same Day        |   547|

## Country/Region by orders:
|United States  |  9994|
|Canada         |  200|

## Top 5 cities by orders:
|New York City   | 915|
|Los Angeles     | 747|
|Philadelphia    | 537|
|San Francisco   | 510|
|Seattle         | 428|

## Top 5 postal codes by orders:
|10035  |  263|
|10024  |  230|
|10009  |  229|
|94122  |  203|
|10011  |  193|

## Division by orders:
|Chocolate  |  9844|
|Other      |   310|
|Sugar      |    40|

## Regions by orders:
|Pacific  |   3253|
|Atlantic |   2986|
|Interior |   2335|
|Gulf     |   1620|

## Top 5 product IDs by orders:
|CHO-MIL-31000  |  2137|
|CHO-SCR-58000  |  2064|
|CHO-TRI-54000  |  2015|
|CHO-FUD-51000  |  1818|
|CHO-NUT-13000  |  1810|

## Top 5 products by orders:
|Wonka Bar - Milk Chocolate        |   2137|
|Wonka Bar -Scrumdiddlyumptious    |   2064|
|Wonka Bar - Triple Dazzle Caramel |   2015|
|Wonka Bar - Fudge Mallows         |   1818|
|Wonka Bar - Nutty Crunch Surprise |   1810|

## Factory counts:
Factory Name
|Lot's O' Nuts       | 5692|
|Wicked Choccy's     | 4152|
|Secret Factory      |  217|
|The Other Factory   |  100|
|Sugar Shack         |   27|
|Unknown Factory     |  6|

## Product Counts:
|Wonka Bar - Milk Chocolate        |   2137|
|Wonka Bar -Scrumdiddlyumptious    |   2064|
|Wonka Bar - Triple Dazzle Caramel |   2015|
|Wonka Bar - Fudge Mallows         |   1818|
|Wonka Bar - Nutty Crunch Surprise |   1810|
|Wonka Gum                         |   120|
|Kazookles                         |    96|
|Lickable Wallpaper                |    94|
|Laffy Taffy                       |    10|
|SweeTARTS                         |    10|
|Fizzy Lifting Drinks              |     6|
|Nerds                             |     4|
|Hair Toffee                       |     4|
|Everlasting Gobstopper            |      3|
|Fun Dip                           |      3|

## Division Counts:
|Chocolate  |  9844|
|Other      |   310|
|Sugar      |    40|

##New features engineered:
| | Feature Name|
|1| Shipping Lead Time|
|2| Factory Name|
|3| Factory Location|
|4| Profit Margin %|