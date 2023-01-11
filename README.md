# PipelineSerializer

PipelineSerializer is a meltano utility extension for serializing parts of a pipeline (e.g. dbt).

# Installation
Run `meltano add --custom utilities [mutexname]`. Name the plugin whatever you want to call your mutex in your pipelines. Specify `git+https://github.com/tombriggsallego/meltano-pipeline-serializer.git` as the pip_url and `serializer` as the executable.

# Usage
Put lock and unlock commands around parts of the pipeline you want to be mutually exclusive. For example, if you named your plugin dbtmutex and you want to make sure only one instance of dbt is running at a time, do:

`meltano run tap-something mapper-something target-something dbt-postgres:deps dbtmutex:lock dbt-postgres:run dbtmutex:unlock`

Use the maxattempts and sleepseconds options to control how many times the plugin should attempt to acquire the lock and how long it should wait between attempts, respectively. Setting maxattempts to 0 means "try forever".

NOTE: Once the number of attempts is exhausted, an exception will be raised. This will cause the rest of your pipeline to stop! If you're using this plugin to ensure only one instance of dbt runs at the end of an otherwise-successful pipeline that is the behavior you want, however.

# Configuration
```yaml
plugins:
  utilities:
  - name: dbtmutex
    namespace: serializer
    pip_url: git+https://github.com/tombriggsallego/meltano-pipeline-serializer.git
    executable: serializer
    settings:
    - name: serializer_max_attempts
      kind: integer
      value: 6
      description: How many times to try to get the lock
      env: SERIALIZER_MAX_ATTEMPTS
    - name: serializer_sleep_seconds
      kind: integer
      value: 10
      description: How long to wait between lock attempts
      env: SERIALIZER_SLEEP_SECONDS
    - name: serializer_file_name
      value: dbtmutex.lck
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


