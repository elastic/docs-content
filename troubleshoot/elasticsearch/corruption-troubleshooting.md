---
navigation_title: Data corruption
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/corruption-troubleshooting.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Troubleshoot data corruption [corruption-troubleshooting]

{{es}} expects that the data it reads from disk is exactly the data it previously wrote. If it detects that the data on disk is different from what it wrote then it will report some kind of exception such as:

* `org.apache.lucene.index.CorruptIndexException`
* `org.elasticsearch.gateway.CorruptStateException`
* `org.elasticsearch.index.translog.TranslogCorruptedException`

Typically these exceptions happen due to a checksum mismatch. Most of the data that {{es}} writes to disk is followed by a checksum using a simple algorithm known as CRC32 which is fast to compute and good at detecting the kinds of random corruption that may happen when using faulty storage. A CRC32 checksum mismatch definitely indicates that something is faulty, although of course a matching checksum doesn’t prove the absence of corruption.

Verifying a checksum is expensive since it involves reading every byte of the file which takes significant effort and might evict more useful data from the filesystem cache, so systems typically don’t verify the checksum on a file very often. This is why you tend only to encounter a corruption exception when something unusual is happening. For instance, corruptions are often detected during merges, shard movements, and snapshots. This does not mean that these processes are causing corruption: they are examples of the rare times where reading a whole file is necessary. {{es}} takes the opportunity to verify the checksum at the same time, and this is when the corruption is detected and reported. It doesn’t indicate the cause of the corruption or when it happened. Corruptions can remain undetected for many months.

The files that make up a Lucene index are written sequentially from start to end and then never modified or overwritten. This access pattern means the checksum computation is very simple and can happen on-the-fly as the file is initially written, and also makes it very unlikely that an incorrect checksum is due to a userspace bug at the time the file was written. The part of {{es}} that computes the checksum is straightforward, widely used, and very well-tested, so you can be very confident that a checksum mismatch really does indicate that the data read from disk is different from the data that {{es}} previously wrote.

If a file header is corrupted then it’s possible that {{es}} might not be able to work out how to even start reading the file which can lead to an exception such as:

* `org.apache.lucene.index.IndexFormatTooOldException`
* `org.apache.lucene.index.IndexFormatTooNewException`

It is also possible that {{es}} reports a corruption if a file it needs is entirely missing, with an exception such as:

* `java.io.FileNotFoundException`
* `java.nio.file.NoSuchFileException`

The files that make up a Lucene index are written in full before they are used. If a file is needed to recover an index after a restart then your storage system previously confirmed to {{es}} that this file was durably synced to disk. On Linux this means that the `fsync()` system call returned successfully. {{es}} sometimes reports that an index is corrupt because a file needed for recovery is missing, or it exists but has been truncated or is missing its footer. This may indicate that your storage system acknowledges durable writes incorrectly.

There are many possible explanations for {{es}} detecting corruption in your cluster. Databases like {{es}} generate a challenging I/O workload that may find subtle infrastructural problems which other tests may miss. {{es}} is known to expose the following problems as file corruptions:

* Filesystem bugs, especially in newer and nonstandard filesystems which might not have seen enough real-world production usage to be confident that they work correctly.
* [Kernel bugs](https://www.elastic.co/blog/canonical-elastic-and-google-team-up-to-prevent-data-corruption-in-linux).
* Bugs in firmware running on the drive or RAID controller.
* Incorrect configuration, for instance configuring `fsync()` to report success before all durable writes have completed.
* Faulty hardware, which may include the drive itself, the RAID controller, your RAM or CPU.
* Third-party software which modifies the files that {{es}} writes.

Data corruption typically doesn’t result in other evidence of problems apart from the checksum mismatch. Do not interpret this as an indication that your storage subsystem is working correctly and therefore that {{es}} itself caused the corruption. It is rare for faulty storage to show any evidence of problems apart from the data corruption, but data corruption itself is a very strong indicator that your storage subsystem is not working correctly.

To rule out {{es}} as the source of data corruption, generate an I/O workload using something other than {{es}} and look for data integrity errors. On Linux the `fio` and `stress-ng` tools can both generate challenging I/O workloads and verify the integrity of the data they write. Use version 0.12.01 or newer of `stress-ng` since earlier versions do not have strong enough integrity checks. Verify that durable writes persist across power outages using a script such as [`diskchecker.pl`](https://gist.github.com/bradfitz/3172656). Alternatively, use a tool such as `strace` to observe the sequence of syscalls that {{es}} makes when writing data and confirm that this sequence does not explain the reported corruption.

To narrow down the source of the corruptions, systematically change components in your cluster’s environment until the corruptions stop. The details will depend on the exact configuration of your environment, but may include the following:

* Try a different filesystem or a different kernel.
* Try changing each hardware component in turn, ideally changing to a different model or manufacturer.
* Try different firmware versions for each hardware component.
* Remove any third-party software which may modify the contents of the {{es}} data path.

