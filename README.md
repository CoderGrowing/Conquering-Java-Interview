# Java 常见面试题及答案

[TOC]

# 一、Java 基础

## JDK 和 JRE 有什么区别？

JDK 包括了 Java 程序设计语言、Java 虚拟机和 Java API 类库这三部分，是用于支持 Java 开发的最小环境。

JRE 包括 Java API 类库中的 Java SE API 子集和 Java 虚拟机两部分，是支持 Java 程序运行的标准环境。

## equals 和 == 有什么区别？

**==**

> 关系操作符生成的是一个 boolean 结果，它们计算的是操作数的值之间的关系
>
> 《Java 编程思想》

毫无疑问 == 就是一个关系操作符，所以使用 == 计算的是操作数的值之间的关系。

```java
// ①
3 == 3; // true

// ②
String s1 = new String("string");
String s2 = new String("string");
s1 == s2;	// false
```

对于第一种情况，即基本类型，== 直接计算两个操作数之间的关系，返回 true。而对于第二种情况，String 并不是基本类型，存储的不是值，而是所关联的对象在内存中的地址。所以 == 返回 false。（需要注意由于有 String pool 的存在，直接比较 `"String" == "String"` 的话会返回 true。

**equals**

```java
// java.lang.Object

public boolean equals(Object obj) {
    return this == obj;
}
```

由 Object.java 的源代码可以看到 equals 方法是用来比较两个对象的引用是否相等，即是否指向同一个对象，行为和 == 相同。 但大多数的类都会重写 Object 提供的 equals 方法，String 类也不例外，下面我们来看看 String 类的 equals 方法实现：

```java
public boolean equals(Object anObject) {
    if (this == anObject) {
        return true;
    }
    if (anObject instanceof String) {
        String anotherString = (String)anObject;
        int n = value.length;
        if (n == anotherString.value.length) {
            char v1[] = value;
            char v2[] = anotherString.value;
            int i = 0;
            while (n-- != 0) {
                if (v1[i] != v2[i])
                    return false;
                i++;
            }
            return true;
        }
    }
    return false;
    }
```

重写后的 equals 方法比较的是字符串中每个字符是否相等。

**总结**

对于 ==，如果作用于基本数据类型的变量，则直接比较其存储的 “值”是否相等；如果作用于引用类型的变量，则比较的是所指向的对象的地址。

对于 equals 方法，如果没有对 equals 方法进行重写，则比较的是引用类型的变量所指向的对象的地址；重写过的 equals 方法比较的一般是对象的值。

## 为什么重写 equals 方法必须重写 hashcode 方法？

默认的 hashCode 方法会利用对象的地址来计算 hashcode 值，不同对象的 hashcode 值是不一样的。 

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

可以看出 Object 类中的 equals 方法与“ == ”是等价的，也就是说判断对象的地址是否相等。Object 类中的 equals 方法进行的是基于内存地址的比较。 

一般对于存放到 Set 集合或者 Map 中键值对的元素，需要按需要重写 hashCode 与 equals 方法，以保证唯一性。

## String 为何不可变？如何实现的不可变？

**如何实现的不可变**

```java
public final class String  implements java.io.Serializable, Comparable<string>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
    // ...
}
```

首先，String 类被声明为 final，即不可继承，其他类无法通过继承来改变 String 的行为。

其次，String 在底层是通过 char 类型字符数组 value 来实现存储的，value 同样被设置为了 final，表明 stack 里的这个叫 value 的字符数组引用地址不可变 ，即无法引用其他数组。

最后，String 的方法里都很小心的没有去动 value 里的元素，而且没有对外暴露内部成员字段，所以外部方法无法更改 value 内存储的值。从这三个方面保证了 String 的不可变。

**为何不可变**

**1. 可以缓存 hash 值** 

因为 String 的 hash 值经常被使用，例如 String 用做 HashMap 的 key。不可变的特性可以使得 hash 值也不可变，因此只需要进行一次计算。

**2. String Pool 的需要** 

如果一个 String 对象已经被创建过了，那么就会从 String Pool 中取得引用。只有 String 是不可变的，才可能使用 String Pool。

![](assets/f76067a5-7d5f-4135-9549-8199c77d8f1c.jpg)

**3. 安全性** 

String 经常作为参数，String 不可变性可以保证参数不可变。例如在作为网络连接参数的情况下如果 String 是可变的，那么在网络连接过程中，String 被改变，改变 String 对象的那一方以为现在连接的是其它主机，而实际情况却不一定是。

**4. 线程安全** 

String 不可变性天生具备线程安全，可以在多个线程中安全地使用。

> [Why String is immutable in Java?](https://www.programcreek.com/2013/04/why-string-is-immutable-in-java/)

## StringBuilder 和 StringBuffer 有什么区别？应用场景？

**为何要用到 StringBuilder 或 StringBuffer**

有时候需要用多个较短的字符构建字符串。因为字符串时不可变的，所以每次连接字符串都会构建新的 String 对象，既耗时也浪费空间。此时可以采用 StringBuffer 或者 StringBuilder 来解决这个问题。

```java
StringBuilder builder = new StringBuilder();
builder.append("hello, ");
builder.append("world.");
```

构建完成后，调用 `toString()` 方法就可以得到一个 String 对象：

```java
String resultString = builder.toString();
```

**StringBuilder 和 StringBuffer 的区别**

StringBuffer 的效率较低，但允许多线程执行添加或删除字符的操作。

StringBuilder 类是 JDK5.0 引入的 StringBuffer 改进版，它的效率高，但无法并发操作。它们两个的 API 是相同的。

**常用方法**

下面拿 StringBuilder 当做例子来说明常用 API：

- `StringBuilder`：构建一个空的 StringBuilder
- `length()`：返回 StringBuilder 中的代码单元数量
- `append(char c)`：添加一个代码单元并返回 this
- `append(String str)`：添加一个字符串并返回 this
- `setCharAt(int i, char c)`：将第 i 个代码单元设置为 c
- `toString()`：构建字符串

## Xmx 和 Xms如何使用？

Xmx 和 Xms 是 Java 虚拟机启动时的可选参数。

Xmx 指定 Java 虚拟机最大可分配内存，超出此内存将会产生 OutOfMemoryError 异常。Xmx 通常具有默认值 256 MB。 

Xms 指定 Java 虚拟机初始化时占用的内存大小，此项一般没有默认值。

## ArrayList 和 LinkedList 的区别？

1. ArrayList 是实现了基于**动态数组**的数据结构，LinkedList 基于**双向链表**的数据结构。    
2. 对于随机访问 get 和 set，ArrayList 优于 LinkedList，因为 LinkedList 要移动指针。    
3. 对于新增和删除操作 add 和 remove，LinedList 比较占优势，因为 ArrayList 要移动数据。

## 什么是多态？如何体现多态？

正如字面上的意思，多态就是**事物在运行过程中存在多种的状态。**多态的体现需要有三个前提：

1. 要有继承关系 （或者实现接口）
2. 子类要重写父类的方法
3. 父类引用指向子类

例子：

```java
class Person {
    void run() {
        System.out.println(" 人在跑 ");
    }
}

class Student extends Person {
    @Override
    void run() {
        System.out.println(" 学生在奔跑 ");
    }
}

public static void main(String[] args) {
    Person p = new Student();
    p.run();    // 学生在奔跑
}
```

父类引用指向子类对象，调用方法时会调用子类的实现，而不是父类的实现，这就叫多态。 

注意上述的例子是**方法重写**（override），而**方法重载**（overload）并不体现多态。

# 二、JMM 与并发

# 三、JVM

# 四、框架

# 五、数据库

# 六、算法

# 七、其他

 