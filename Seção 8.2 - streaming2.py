from pyspark.sql import SparkSession

if __name__ == "__main__":
	spark = SparkSession.builder.appName('Streaming2').getOrCreate()
	
	jsonschema = "nome STRING, postagem STRING, data INT"
	
	df = spark.readStream.json("/home/vinicius/testestream/", schema=jsonschema)
	
	diretorio = "/home/vinicius/temp/"
	
	def atualizapostgres(dataf, batchId):
		dataf.write.format("jdbc")\
		.option("url","jdbc:postgresql://localhost:5432/posts")\
		.option("dbtable","posts")\
		.option("user","postgres")\
		.option("password","813915")\
		.option("driver","org.postgresql.Driver")\
		.mode("append")\
		.save()
	
	stcal = df.writeStream.foreachBatch(atualizapostgres)\
	.outputMode('append')\
	.trigger(processingTime='5 second')\
	.option("checkpointlocation", diretorio)\
	.start()
	
	stcal.awaitTermination()
		
		
		
		
