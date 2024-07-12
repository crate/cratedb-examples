import scalaj.http.{Http, HttpOptions}
import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types._
import org.json4s.jackson.Serialization
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.sql.Timestamp

object SparkCrateDBhttpExample {
  def main(args: Array[String]): Unit = {
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
	
	val data = Seq(
	  Row(Timestamp.valueOf(LocalDateTime.parse("2024-07-10 10:00", formatter)), Array(9.744417, 47.413417), """{"example_quantity_field": 30, "example_string_field": "abc"}"""),
	  Row(Timestamp.valueOf(LocalDateTime.parse("2024-07-10 11:00", formatter)), Array(13.46738, 52.50463), """{"example_quantity_field": 40, "example_string_field": "def"}""")
	)
	
	val spark = SparkSession.builder
		.appName("test")
		.master("local[*]") 
		.getOrCreate()
	val df = spark.createDataFrame(
	  spark.sparkContext.parallelize(data),
	  StructType(
		List(
		  StructField("examplefield1", TimestampType, true),
		  StructField("anotherfield", ArrayType(DoubleType), true),
		  StructField("jsonpayload", StringType, true)
		)
	  )
	)
	
	val url = "http://localhost:4200/_sql"
	
	val columns = df.columns.mkString(", ")
	val placeholders = df.columns.map(_ => "?").mkString(", ")
	val stmt = s"INSERT INTO myschema.mytable ($columns) VALUES ($placeholders)"

	val columnNames = df.columns
	df.foreachPartition { partition =>  
	  val bulkArgs: List[List[Any]] = partition.map { row =>
		columnNames.indices.map(i => row.get(i)).toList
	  }.toList

	  if (bulkArgs.nonEmpty) {    
		val data = Map(
		  "stmt" -> stmt,
		  "bulk_args" -> bulkArgs
		)
			
		implicit val formats = org.json4s.DefaultFormats
		val jsonString = Serialization.write(data)
		
		val response = Http(url)
		  .postData(jsonString)
		  .header("Content-Type", "application/json")      
		  .asString
		
		println(response)
	  }
	}	
  }
}

