name := "SparkCrateDBhttpExample"

version := "0.1"

scalaVersion := "2.11.12"

libraryDependencies ++= Seq(
  "org.scala-lang.modules" %% "scala-xml" % "1.0.6",
  "org.scalaj" %% "scalaj-http" % "2.4.2",  
  "org.apache.spark" %% "spark-sql" % "2.4.8"
)
