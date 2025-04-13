from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import matplotlib.pyplot as plt
from pyspark import SparkConf, SparkContext

# Configuration Spark
conf = SparkConf().setAppName("SentimentAnalysis").setMaster("local[*]") \
    .set("spark.executor.memory", "4g") \
    .set("spark.driver.memory", "4g")
sc = SparkContext(conf=conf)

# 1. Créer une SparkSession
spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .getOrCreate()

# 2. Charger les données
df = spark.read.csv("data/Reviews.csv", header=True, inferSchema=True)
df = df.select("Text", "Score").na.drop()

# 3. Créer la colonne Sentiment
df = df.withColumn("Sentiment", when(col("Score") <= 2, "negative")
                   .when(col("Score") == 3, "neutral")
                   .otherwise("positive"))

# 4. Indexer le label
indexer = StringIndexer(inputCol="Sentiment", outputCol="label")

# 5. Prétraitement texte
tokenizer = Tokenizer(inputCol="Text", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
idf = IDF(inputCol="rawFeatures", outputCol="features")

# 6. Modèle
lr = LogisticRegression(maxIter=10, regParam=0.001)

# 7. Pipeline
pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf, lr])

# 8. Split données
(training, test) = df.randomSplit([0.8, 0.2], seed=42)

# 9. Entraînement
model = pipeline.fit(training)

# 10. Évaluation
predictions = model.transform(test)
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

# 11. Sauvegarde résultats
with open("output/results.txt", "w", encoding="utf-8") as f:
    f.write(f"Accuracy: {accuracy:.2f}\n")
    f.write("Exemples de prédictions :\n")
    for row in predictions.select("Text", "Sentiment", "prediction").take(5):
        f.write(f"Texte: {row.Text[:100]}... => Sentiment prédit: {int(row.prediction)}\n")

# 12. Graphe
# Compter les sentiments
sentiment_counts = predictions.groupBy("Sentiment").count().collect()
sentiment_map = {"negative": 0, "neutral": 0, "positive": 0}
for row in sentiment_counts:
    sentiment_map[row["Sentiment"]] = row["count"]

labels = ["Négatif", "Neutre", "Positif"]
values = [sentiment_map["negative"], sentiment_map["neutral"], sentiment_map["positive"]]

plt.bar(labels, values, color=["red", "gray", "green"])
plt.title("Répartition des sentiments")
plt.xlabel("Sentiment")
plt.ylabel("Nombre de prédictions")
plt.tight_layout()
plt.savefig("output/results.png")
plt.show()

print(f"✅ Analyse terminée. Précision: {accuracy:.2f}")
spark.stop()
model.write().overwrite().save("output/model")
