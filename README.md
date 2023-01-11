# PipelineSerializer

PipelineSerializer is a meltano utility extension for serializing parts of a pipeline (e.g. dbt).

# Installation
Run `meltano add --custom utilities` and specify `git+https://github.com/tombriggsallego/meltano-pipeline-serializer.git` as the pip_url.

# Configuration
```yaml
plugins:
  utilities:
  - name: mymutex
    namespace: serializer
    pip_url: git+https://github.com/tombriggsallego/meltano-pipeline-serializer.git
    executable: serializer
    settings:
    - name: serializer_max_attempts
      kind: integer
      value: 6
      description: How many times to try to get the lock
      env: SERIALIZER_MAX_ATTEMPTS
    - name: serializer_sleep_time
      kind: integer
      value: 10
      description: How long to wait between lock attempts
      env: SERIALIZER_SLEEP_SECONDS
    - name: serializer_file_name
      value: mymutex.lck
      description: Name of the file to use for locking
      env: SERIALIZER_FILE_NAME
    commands:
      lock:
        args: lock
        description: Acquire a lock
      unlock:
        args: unlock
        description: Release a lock
```


