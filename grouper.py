def grouper(data, cluster_size=2):
    return [data[i:i+cluster_size] for i in range(0, len(data), cluster_size)]


for i in xrange(1000000):
   print "/".join(grouper("%06d" % i, 2))
