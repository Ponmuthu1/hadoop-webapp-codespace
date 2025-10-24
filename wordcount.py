from mrjob.job import MRJob


class MRWordCount(MRJob):
    """Simple WordCount using pure Python MapReduce"""

    def mapper(self, _, line):
        # Split each line into words
        for word in line.strip().split():
            yield word.lower(), 1

    def reducer(self, word, counts):
        # Sum all counts for each word
        yield word, sum(counts)


if __name__ == "__main__":
    MRWordCount.run()
