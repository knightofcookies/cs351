> hadoop jar "C:\Users\ahlad\Downloads\Installers\hadoop-3.4.0\hadoop-3.4.0\share\hadoop\tools\lib\hadoop-streaming-3.4.0.jar" -input big.txt -output big_output -mapper mapper.py -combiner combiner.py -reducer reducer.py
> hadoop jar $HADOOP_HOME/hadoop-streaming.jar input output -mapper mapper.py -reducer reducer.py
> hadoop jar hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount input output

> hadoop jar hadoop-streaming-3.2.1.jar -input big.txt -output big_output -mapper mapper.py -combiner combiner.py -reducer reducer.py

