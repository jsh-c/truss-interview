import sys
import re
from datetime import datetime
from datetime import timedelta

def parse_line(line):
    # Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
    fields = parse_fields(line)
    fields[0] = normalize_timestamp(fields[0])
    fields[2] = normalize_zipcode(fields[2])
    fields[3] = normalize_name(fields[3])
    foo_duration = normallize_duration(fields[4])
    bar_duration = normallize_duration(fields[5])
    fields[4] = str(foo_duration)
    fields[5] = str(bar_duration)
    fields[6] = str(foo_duration + bar_duration)

    return ",".join(fields)

def parse_fields(line):
  # find the fileds with qouted string if any; could have multiple quotes per line
  quoted = re.findall(r'\"(.*?)\"', line)
  if quoted:
    for q in quoted:
      # get rid of the qouted string for easier parsing
      line = line.replace('"' + q + '"', "")

  fields = line.split(",")

  # put back the qouted string to where it belonged
  j = 0
  for i, field in enumerate(fields):
    if not field and j < len(quoted):
      fields[i] = '"' + quoted[j] + '"'
      j += 1

  return fields

def normalize_timestamp(datetime_str):
  dt = datetime.strptime(datetime_str, "%m/%d/%y %I:%M:%S %p") + timedelta(hours=3)
  return str(dt)

def normalize_zipcode(zipcode):
  return zipcode.zfill(5)

def normalize_name(name):
  return name.upper()

def normallize_duration(duration):
  times = re.match(r'(\d+):(\d+):(\d+)\.(\d+)', duration)
  td = timedelta(hours=int(times.group(1)), minutes=int(times.group(2)), seconds=int(times.group(3)), milliseconds=int(times.group(4)))
  return td.total_seconds()



if __name__ == "__main__":
  try:
    count = 0
    data = sys.stdin.buffer.read().decode('utf-8', 'replace')
    lines = re.findall(r'(.*)\r?\n', data)
    for line in lines:
      # the header
      if count == 0:
        print(line)
        count += 1
        continue

      print(parse_line(line))
      count += 1

  except KeyboardInterrupt:
    sys.stdout.flush()
    pass
