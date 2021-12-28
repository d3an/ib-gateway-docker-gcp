# Interactive Brokers Gateway in Docker ![Build Status](https://github.com/dvasdekis/ib-gateway-docker-gcp/workflows/Test%20and%20Publish/badge.svg "Build Status")

### Latest Versions

* **IB Gateway:** `v10.12.2d`
* **IBC:** `v3.12.0`
* **ib_insync:** `v0.9.70`

<br/>

### Getting Started

1. Download the IB Gateway (Linux 64-bit) latest installation script from [here](https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-linux-x64.sh) or run the following command from the project directory:
```commandline
wget -O ibgateway-stable-standalone-linux-1012-2d-x64.sh https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-linux-x64.sh
```
2. Make sure the script is renamed to `ibgateway-stable-standalone-linux-${TWS_MAJOR_VRSN}-${TWS_MINOR_VRSN}-x64.sh`.
3. Update `Dockerfile`'s environment variables with the corresponding `TWS_MAJOR_VRSN` and `TWS_MINOR_VRSN`.
4. Set `TWS_USER_ID` and `TWS_PASSWORD` respectively in your system's environment.
5. Run the following:
```commandline
docker-compose up --build
```

You will now have the IB Gateway app running on port 4003 for Live trading and 4004 for Paper trading. See [docker-compose.yml](docker-compose.yml) for configuring VNC password, accounts and trading mode.

**WARNING:** All IPs on your network are able to connect to your box and place trades - so please do not open your box to the internet.

<br/>

### History

This repo is built on [mvberg's](https://github.com/mvberg/ib-gateway-docker) and [dvasdekis's](https://github.com/dvasdekis/ib-gateway-docker-gcp) work.

#### dvasdekis

* Replaced IB Controller with IBC
* Ubuntu 16.04 → 20.04
* Removed installers after use
* Compatible with Stackdriver logging
* Optimization of Java runtime options
* VNC scripting (which didn't restart the container on error) fixed via Supervisor
* Optimized for e2-small instance on GCP

#### d3an

* Example usage for dual paper/live containers
* Minor refactors and abstractions
* Version updates

<br/>

### Docker Hub Image (Expired)

* [dvasdekis/ib-gateway-docker](https://hub.docker.com/r/dvasdekis/ib-gateway-docker)

To start an instance on Google Cloud:
`gcloud compute instances create-with-container my-ib-gateway --container-image="docker.io/dvasdekis/ib-gateway-docker:v978" --container-env-file="./ibgateway.env" --machine-type=e2-small --container-env TWSUSERID="$tws_user_id",TWSPASSWORD="$tws_password",TRADING_MODE=paper --zone="my-preferred-zone"`

#### Logging in with VNC:

1. Uncomment the lines marked 'ports' in docker-compose
2. SSH into server and run `mkdir ~/.vnc && echo "mylongpassword" > ~/.vnc/passwd && x11vnc -passwd mylongpassword -display ":99" -forever -rfbport 5900` as root
3. Log in with a remote VNC client using `mylongpassword` on port 5901

<br/>

### Troubleshooting

##### Read-Only API warning:
IBC has decided to not support switching off the Read-Only checkbox (on by default) on the API Settings page.

To work around it for some operations, you'll need to write a file named `ibg.xml` to `/root/Jts/*encrypted user id*/ibg.xml`. The ibg.xml file can be found in this folder after a successful run and close, and contains the application's settings from the previous run.

##### 
Sometimes, when running in non-daemon mode, you'll see this:

```java
Exception in thread "main" java.awt.AWTError: Can't connect to X11 window server using ':0' as the value of the DISPLAY variable.
```

You will have to remove the container `docker rm container_id` and run `docker-compose up` again.
