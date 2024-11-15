from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql.functions import trim, lower

spark = SparkSession.builder.appName("Apache Spark").getOrCreate()

data = spark.read.csv("adult.data", header=False, inferSchema=True)

columns = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "income",
]
data = data.toDF(*columns)
data = data.replace("?", None).dropna()


indexer_workclass = StringIndexer(inputCol="workclass", outputCol="workclass_indexed")
indexer_education = StringIndexer(inputCol="education", outputCol="education_indexed")
data = indexer_workclass.fit(data).transform(data)
data = indexer_education.fit(data).transform(data)


assembler = VectorAssembler(
    inputCols=["age", "workclass_indexed", "education_indexed"], outputCol="features"
)
data_with_features = assembler.transform(data)


kmeans = KMeans(k=3, seed=1)
model = kmeans.fit(data_with_features)
clusters = model.transform(data_with_features)
clusters.select("age", "workclass", "education", "prediction").show(5)


country_counts = (
    data.filter(
        (lower(trim(data["native-country"])) != "united-states") & (data["age"] >= 18)
    )
    .groupBy("native-country")
    .count()
    .orderBy("count", ascending=False)
)
top_country = country_counts.first()
print(
    "Country with highest number of adults (except USA):",
    top_country["native-country"],
)

masters_tech_support = data.filter(
    (lower(trim(data["education"])).isin("masters", "doctorate", "prof-school"))
    & (lower(trim(data["occupation"])) == "tech-support")
).count()

print(
    "Number of people with at least a masters degree and working in tech support:",
    masters_tech_support,
)

unmarried_local_gov_males = data.filter(
    (lower(trim(data["sex"])) == "male")
    & (lower(trim(data["relationship"])) == "not-in-family")
    & (lower(trim(data["workclass"])) == "local-gov")
).count()

print("Number of unmarried males working in Local_govt:", unmarried_local_gov_males)
