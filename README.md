## BBW

**BBW** is a little script that fetches all the latest writeups from pentester land.
The special thing about **BBW** is that it keeps track of the latest writeup you read after running the script, so that is always gives you the writeups that are new for you to read.

## INSTALLATION

```bash
$ git clone https://github.com/N3H4L/bbw.git
$ cd bbw
$ pip install -r requirements.txt
```

Now, **BBW** is ready for you to run.

## RUNNING BBW

You can run **BBW** in cron mode by simply:

```bash
$ python bbw.py
```

In cron mode, the script checks if there is a new writeup at an interval of 1 hour. If there is you will see the latest writeups.

You can also run **BBW** without cron by giving a CLI argument `nocron`:

```bash
$ python bbw.py nocron
```

In nocron mode, you will get instant result if there is a new writeup.