---
title: Golang字符串的实现
date: 2022-08-26 15:34:30
tags: Golang
categories: Golang
---

## 字符串的本质
在Go中，字符串不能被修改，只能被访问。

字符串的终结方式：

1. C语言中隐式声明，以'\0'结尾
2. Go中显示声明
```golang
type StringHeader struct{
    Data uintptr
    Len  int
}
```
Data指向底层数组，Len表示长度。字符串在本质上是一串字符的数组，每个字符在存储时对应**一个或多个整数**。

Go中采用UTF-8编码，是**可变长**编码，字母占1字节，中文占3字节，`len("GO语言")`的长度为8。

## 符文类型rune
Go语言设计者认为，用字符表示字符串的组成元素会产生歧义，Go使用符文类型**rune**来表示和区分“字符”，**rune是int32的别称**。

使用range轮询时，轮询的是rune。
```golang
b := "Go语言"
for index, runeValue := range b{
    ...
}
```
index代表字节偏移，runeValue为int32，代表符文数。
可以使用"%#U"打印。

## 字符串工具函数
### strings
- `func Clone(s string) string`
- `func Contains(s, substr string) bool`
- `func EqualFold(s, t string) bool` 不区分大小写是否相等
- `func Fields(s string) []string` 空格分隔
- `func FieldsFunc(s string, f func(rune) bool) []string` 函数为true分割
- `func Split(s, sep string) []string`

### strconv
- `func FormatInt(i int64, base int) string`
- `func ParseInt(s string, base int, bitSize int) (i int64, err error)`
- `func Atoi(s string) (int, error)` Atoi等价于ParseInt(s, 10,0)，转换为int类型。


## string和byte[]互转

### StringHeader和SliceHeader
``` golang
type StringHeader struct {  
    Data uintptr    
    Len  int    
}   

type SliceHeader struct {   
    Data uintptr    
    Len  int    
    Cap  int    
}
```
### string转[]byte

```golang
func stringTobytes(s string) []byte {
    str := (*reflect.StringHeader)(unsafe.Pointer(&s))
    by := reflect.SliceHeader{
        Data: str.Data,
        Len:  str.Len,
        Cap:  str.Len,
    }
    return *(*[]byte)(unsafe.Pointer(&by))
}
```
### []byte转string
```golang
func byteToString(b []byte) string {
    return *(*string)(unsafe.Pointer(&b))
}

// 或者

func byteToString(b []byte) string {
    by := (*reflect.SliceHeader)(unsafe.Pointer(&b))

    str := reflect.StringHeader{
        Data: by.Data,
        Len:  by.Len,
    }
    return *(*string)(unsafe.Pointer(&str))
}
```