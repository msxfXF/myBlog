---
title: CWE漏洞检测
date: 2022-07-11 08:34:59
tags:
categories:
---

## CWE-Checker

https://github.com/fkie-cad/cwe_checker

支持检测

- CWE-78: OS Command Injection (currently disabled on standard runs)
- CWE-119 and its variants CWE-125 and CWE-787: Buffer Overflow
- CWE-134: Use of Externally-Controlled Format String
- CWE-190: Integer Overflow or Wraparound
- CWE-215: Information Exposure Through Debug Information
- CWE-243: Creation of chroot Jail Without Changing Working Directory
- CWE-332: Insufficient Entropy in PRNG
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition
- CWE-416: Use After Free and its variant CWE-415: Double Free
- CWE-426: Untrusted Search Path
- CWE-467: Use of sizeof() on a Pointer Type
- CWE-476: NULL Pointer Dereference
- CWE-560: Use of umask() with chmod-style Argument
- CWE-676: Use of Potentially Dangerous Function
- CWE-782: Exposed IOCTL with Insufficient Access Control

## BinAbsInspector

https://github.com/KeenSecurityLab/BinAbsInspector

- CWE78 (OS Command Injection)
- CWE119 (Buffer Overflow (generic case))
- CWE125 (Buffer Overflow (Out-of-bounds Read))
- CWE134 (Use of Externally-Controlled Format string)
- CWE190 (Integer overflow or wraparound)
- CWE367 (Time-of-check Time-of-use (TOCTOU))
- CWE415 (Double free)
- CWE416 (Use After Free)
- CWE426 (Untrusted Search Path)
- CWE467 (Use of sizeof() on a pointer type)
- CWE476 (NULL Pointer Dereference)
- CWE676 (Use of Potentially Dangerous Function)
- CWE787 (Buffer Overflow (Out-of-bounds Write))

## Relationships
```
- CWE-707: Improper Neutralization
    - CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
        - CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection')
            - 🎯 🦴CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

- CWE-664: Improper Control of a Resource Through its Lifetime
    - CWE-118: Incorrect Access of Indexable Resource ('Range Error')
        - 🎯 🦴CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer
            - CWE-825: Expired Pointer Dereference
                - 🎯 🦴CWE-416: Use After Free
                - 🦴 CWE-415: Double Free
            - 🦴 CWE-125: Out-of-bounds Read
            - 🦴 CWE-787: Out-of-bounds Write


    - CWE-668: Exposure of Resource to Wrong Sphere
        - 🎯 🦴CWE-134: Use of Externally-Controlled Format String
        - CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
            - 🎯 CWE-215: Insertion of Sensitive Information Into Debugging Code

    - CWE-669: Incorrect Resource Transfer Between Spheres
        - 🎯 CWE-243: Creation of chroot Jail Without Changing Working Directory

    - CWE-673: External Influence of Sphere Definition
        - 🎯 🦴CWE-426: Untrusted Search Path

- CWE-682: Incorrect Calculation
    - 🎯 🦴CWE-190: Integer Overflow or Wraparound
    - 🎯 🦴CWE-467: Use of sizeof() on a Pointer Type

- CWE-693: Protection Mechanism Failure
    - CWE-330: Use of Insufficiently Random Values
        - CWE-331: Insufficient Entropy
            - 🎯 CWE-332: Insufficient Entropy in PRNG

- CWE-691: Insufficient Control Flow Management
    - CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
        - 🎯 🦴CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition
        
    - CWE-749: Exposed Dangerous Method or Function
        - 🎯 CWE-782: Exposed IOCTL with Insufficient Access Control

- CWE-703: Improper Check or Handling of Exceptional Conditions
    - CWE-754: Improper Check for Unusual or Exceptional Conditions
        - 🎯 🦴CWE-476: NULL Pointer Dereference

- CWE-710: Improper Adherence to Coding Standards
    - CWE-1177: Use of Prohibited Code
        - 🎯 🦴CWE-676: Use of Potentially Dangerous Function

```
## Example

### CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

``` c
int main(int argc, char** argv) {
    char cmd[CMD_MAX] = "/usr/bin/cat ";
    strcat(cmd, argv[1]);
    system(cmd);
}
```
However, if an attacker passes a string of the form ";rm -rf /", then the call to system() fails to execute cat due to a lack of arguments and then plows on to recursively delete the contents of the root partition.

### CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer

``` c
int getValueFromArray(int *array, int len, int index) {
int value;
// check that the array index is less than the maximum
// length of the array
if (index < len) {
    // get the value at the specified index of the array
    value = array[index];
}
// if array index is invalid then output error message
// and return value indicating error
else {
    printf("Value is: %d\n", array[index]);
    value = -1;
}
return value;
}
```

However, this method only verifies that the given array index is less than the maximum length of the array **but does not check for the minimum value**.
### CWE-416: Use After Free
``` c
char* ptr = (char*)malloc (SIZE);
if (err) {
    abrt = 1;
    free(ptr);
}
...
if (abrt) {
    logError("operation aborted before commit", ptr);
}
```
### CWE-190: Integer Overflow or Wraparound
``` c
nresp = packet_get_int();
if (nresp > 0) {
    response = xmalloc(nresp*sizeof(char*));
    for (i = 0; i < nresp; i++) response[i] = packet_get_string(NULL);
}
```

### CWE-134: Use of Externally-Controlled Format String
``` c
int main(int argc, char **argv){
char buf[128];
...
snprintf(buf,128,argv[1]);
}
```
### CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition
``` c
#include <sys/types.h>
#include <sys/stat.h>

...

struct stat sb;
stat("MYFILE.txt",&sb);
printf("file change time: %d\n",sb->st_ctime);
switch(sb->st_ctime % 2){
case 0: printf("Option 1\n"); break;
case 1: printf("Option 2\n"); break;
default: printf("this should be unreachable?\n"); break;
}
```

### CWE-676: Use of Potentially Dangerous Function
``` c
void manipulate_string(char * string){
char buf[24];
strcpy(buf, string);
...
}
```