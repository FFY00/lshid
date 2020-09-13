# lshid

Like lsusb, but for HID devices.

```
$ lshid
Device /dev/hidraw0: ID 08bb:2902 Burr-Brown from TI               USB Audio CODEC
Device /dev/hidraw5: ID 046d:405f Logitech Candy
Device /dev/hidraw4: ID 046d:4079 Logitech G Pro
Device /dev/hidraw3: ID 046d:c53a Logitech USB Receiver
Device /dev/hidraw2: ID 046d:c53a Logitech USB Receiver
Device /dev/hidraw1: ID 046d:c53a Logitech USB Receiver
Device /dev/hidraw13: ID 046d:c33c Logitech G513 Carbon Tactile
Device /dev/hidraw12: ID 046d:c33c Logitech G513 Carbon Tactile
```

```
$ lshid -v -s 4
Device /dev/hidraw4: ID 046d:4079 Logitech G Pro
Report Descriptor:
 Usage Page (Generic Desktop Controls)
 Usage (Keyboard)
 Collection (Application)
  Report ID (0x01)
  Report Count (8)
  Report Size (1)
  Logical Minimum (0)
  Logical Maximum (1)
  Usage Page (Keyboard/Keypad)
  Usage Minimum (224)
  Usage Maximum (231)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Report Count (6)
  Report Size (8)
  Logical Minimum (0)
  Logical Maximum (255)
  Usage Page (Keyboard/Keypad)
  Usage Minimum (0)
  Usage Maximum (255)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Report ID (0x0e)
  Usage Page (LED)
  Report Count (5)
  Report Size (1)
  Logical Minimum (0)
  Logical Maximum (1)
  Usage Minimum (1)
  Usage Maximum (5)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Report Count (1)
  Report Size (3)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
 End Collection
 Usage Page (Generic Desktop Controls)
 Usage (Mouse)
 Collection (Application)
  Report ID (0x02)
  Usage (Pointer)
  Collection (Physical)
   Usage Page (Button)
   Usage Minimum (1)
   Usage Maximum (16)
   Logical Minimum (0)
   Logical Maximum (1)
   Report Count (16)
   Report Size (1)
   Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
   Usage Page (Generic Desktop Controls)
   Logical Minimum (32769)
   Logical Maximum (32767)
   Report Size (16)
   Report Count (2)
   Usage (X)
   Usage (Y)
   Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
   Logical Minimum (129)
   Logical Maximum (127)
   Report Size (8)
   Report Count (1)
   Usage (Wheel)
   Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
   Usage Page (Consumer)
   Usage (AC Pan)
   Report Count (1)
   Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  End Collection
 End Collection
 Usage Page (Vendor Page)
 Usage (0x0001)
 Collection (Application)
  Report ID (0x10)
  Report Size (8)
  Report Count (6)
  Logical Minimum (0)
  Logical Maximum (255)
  Usage (0x0001)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Usage (0x0001)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
 End Collection
 Usage Page (Vendor Page)
 Usage (0x0002)
 Collection (Application)
  Report ID (0x11)
  Report Size (8)
  Report Count (19)
  Logical Minimum (0)
  Logical Maximum (255)
  Usage (0x0002)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Usage (0x0002)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
 End Collection
 Usage Page (Vendor Page)
 Usage (0x0004)
 Collection (Application)
  Report ID (0x20)
  Report Size (8)
  Report Count (14)
  Logical Minimum (0)
  Logical Maximum (255)
  Usage (0x0041)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Usage (0x0041)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Report ID (0x21)
  Report Count (31)
  Logical Minimum (0)
  Logical Maximum (255)
  Usage (0x0042)
  Input (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
  Usage (0x0042)
  Output (Data, Array, Absolute, No Wrap, Linear, Preferred State, No Null position, Bit Field)
 End Collection
```
