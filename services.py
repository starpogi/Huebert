
import requests
import json
import time
import random

HOST = '192.168.1.205'

SCALE_CONSTANTS = {
   'h': 65535,
   's': 255,
   'v': 255
}


def turn_off_living_room():
    for light in [5, 6, 7, 8, 10]:
        switch_light(on=False, light=light)

def turn_on_living_room():
    for light in [5, 6, 7, 8, 10]:
        switch_light(on=True, light=light)

def switch_light(on=True, light=20):
    """
    Get the current hsv state of the light, then turn off
    """
    payload = {
       'on': on
    }

    url = 'http://%s/api/newdeveloper/lights/%s/state' % (HOST, light)

    req = requests.put(
       url,
       json=payload
    )

    code = 'OK'

    if req.status_code != 200:
       code = '!! %s !!' % req.status_code

    # print('HUE at [%s, %s, %s] - %s' % (hue, s, v, code))

def set_hsv(hue, saturation, value, on=True):

   if hue == 0 and saturation == 0 and value == 0:
      on = False

   hue, saturation, value = scale(
      hue,
      saturation,
      value
   )

   payload = {
      'on': on,
      'sat': saturation,
      'bri': value,
      'hue': hue
   }

   send_philips(payload, hue=hue, s=saturation, v=value)


def scale(h, s, v):
   h = h * SCALE_CONSTANTS['h'] / 360.0
   s = s * SCALE_CONSTANTS['s'] / 1.0
   v = v * SCALE_CONSTANTS['v'] / 1.0

   return int(h), int(s), int(v)


def send_philips(payload, light=20, hue=0, s=0, v=0):

   data = json.dumps(payload)
   url = 'http://%s/api/newdeveloper/lights/%s/state' % (HOST, light)

   req = requests.put(
      url,
      data=data
   )

   code = 'OK'

   if req.status_code != 200:
      code = '!! %s !!' % req.status_code

   # print('HUE at [%s, %s, %s] - %s' % (hue, s, v, code))


def rgb_to_hsv(red, green, blue):
   r_prime = red/255.0
   g_prime = green/255.0
   b_prime = blue/255.0

   c_list = [r_prime, g_prime, b_prime]
   c_max = max(c_list)
   c_min = min(c_list)
   delta = c_max - c_min

   # Hue
   if not delta:
      hue = 0
   else:
      if c_max == r_prime:
         hue_delta = g_prime - b_prime
         multiplier = (hue_delta / float(delta)) % 6
      elif c_max == g_prime:
         hue_delta = b_prime - r_prime
         multiplier = hue_delta + 2
      elif c_max == b_prime:
         hue_delta = r_prime - g_prime
         multiplier = hue_delta + 4

      hue = 60.0 * multiplier

   # Saturation
   if not c_max:
      saturation = 0
   else:
      saturation = delta / float(c_max)

   # Value
   value = c_max

   return hue, saturation, value


def auth_jb():
   CLIENT_ID = 'T2fexV7pJs4'
   APP_SECRET = '78c628d6a27313fd9abe1a13a5f33d0d5be1cc87'
   url = 'https://jawbone.com/auth/oauth2/auth'

   # auth_payload = {
      # 'client_id': CLIENT_ID,
      # 'client_secret': APP_SECRET,
      # 'grant_type': 'authorization_code',

   # }

   auth_payload = {
      'response_type': 'code',
      'client_id': CLIENT_ID,
      'scope': 'generic_event_read sleep_read heartrate_read',
      'redirect_uri': 'http://127.0.0.1'
   }

   req = requests.post(url, data=json.dumps(auth_payload))

   print(req.text)


if __name__ == '__main__':
   #auth_jb()

   while True:
      r = random.randint(0, 255)
      g = random.randint(0, 255)
      b = random.randint(0, 255)

      h, s, v = rgb_to_hsv(r, g, b)
      set_hsv(h, s, v)
      time.sleep(120)

   #for x in range(0, 65535, 5):
   #
   #   time.sleep(0.15)
