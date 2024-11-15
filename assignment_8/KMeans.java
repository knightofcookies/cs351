import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class KMeans {

    public static class KMeansMapper extends Mapper<Object, Text, Text, Text> {

        private final List<double[]> centroids = new ArrayList<>();

        @Override
        protected void setup(Context context) {
            centroids.add(new double[]{5.8, 4.0});
            centroids.add(new double[]{6.1, 2.8});
            centroids.add(new double[]{6.3, 2.7});
        }


        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split(",");
            if (parts.length >= 2) {
                try {
                    double sepalLength = Double.parseDouble(parts[0]);
                    double sepalWidth = Double.parseDouble(parts[1]);

                    double minDist = Double.MAX_VALUE;
                    int closestCentroid = -1;

                    for (int i = 0; i < centroids.size(); i++) {
                        double[] centroid = centroids.get(i);
                        double dist = euclideanDistance(sepalLength, sepalWidth, centroid[0], centroid[1]);
                        if (dist < minDist) {
                            minDist = dist;
                            closestCentroid = i;
                        }
                    }

                    context.write(new Text(String.valueOf(closestCentroid)), new Text(sepalLength + "," + sepalWidth));
                } catch (NumberFormatException e) {
                    // Handle parsing errors if needed
                }
            }
        }

        private double euclideanDistance(double x1, double y1, double x2, double y2) {
            return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
        }
    }

    public static class KMeansReducer extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            double sumSepalLength = 0;
            double sumSepalWidth = 0;
            int count = 0;

            for (Text val : values) {
                String[] parts = val.toString().split(",");
                sumSepalLength += Double.parseDouble(parts[0]);
                sumSepalWidth += Double.parseDouble(parts[1]);
                count++;
            }

            double avgSepalLength = sumSepalLength / count;
            double avgSepalWidth = sumSepalWidth / count;

            context.write(key, new Text(avgSepalLength + "," + avgSepalWidth));
        }
    }


    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "KMeans");
        job.setJarByClass(KMeans.class);
        job.setMapperClass(KMeansMapper.class);
        job.setReducerClass(KMeansReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);


        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}