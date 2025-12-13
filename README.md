
# unifi-presence

Small flask app that grabs a devices network connection state from a Unifi application


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`UNIFI_URL`- URL of your unifi application e.g https://10.10.10.10:8080

`UNIFI_KEY`- This can ge found in the unifi intergrations section.

`SITE_ID`- ID of site target device is a member of, if site isn't supplied one will be defaulted to.

`DEVICE_NAME` - The name set in unifi of the target device.

`API_HEADER_KEY`- Adds authentication to API, if key is not supplised API will remain open

