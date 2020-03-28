# usb

## Local Development

Requirements:

* Kubernetes (we use [microk8s](https://microk8s.io/) in this example)
* [Skaffold](https://skaffold.dev/)


Bootstrap microk8s:

```
microk8s.kubectl config view --raw > $HOME/.kube/config
microk8s.enable registry ingress dns
```

Start services with Skaffold:

```
skaffold dev --default-repo=localhost:32000
```

Visit the services:

* Appsearch: http://appsearch-127-0-0-1.nip.io/

## Notes

Extract subs:

```
for file in ls **/*.mkv; do ffmpeg -i "$file" "/Users/andy/Projects/andyshinn/usb/subs/$(echo "$file" | pcregrep -io1 '(S\d{2}E\d+(E\d+)?)' | tr '[:upper:]' '[:lower:]').srt"; done
```

Index JSON:

```
for file in ls subs/*.json; do curl -X POST 'http://localhost:3002/api/as/v1/engines/usb/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer private-a23c3jfz4doi7rvy1bi2xvoo' \
  --data-raw "@$file"
done
```

Rename videos:

```
for file in **/*.mkv; do cp "$file" "/Users/andy/Projects/andyshinn/usb/videos/$(echo "$file" | pcregrep -io1 '(S\d{2}E\d+(E\d+)?)' | tr '[:upper:]' '[:lower:]').mkv"; done
```