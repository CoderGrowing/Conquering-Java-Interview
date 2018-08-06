<!-- GFM-TOC -->
* [Java 常见面试题及答案](#java-常见面试题及答案)
* [一、Java 基础](#一java-基础)
    * [JDK 和 JRE 有什么区别？](#jdk-和-jre-有什么区别)
    * [equals 和 == 有什么区别？](#equals-和--有什么区别)
    * [为什么重写 equals 方法必须重写 hashcode 方法？](#为什么重写-equals-方法必须重写-hashcode-方法)
    * [String 为何不可变？如何实现的不可变？](#string-为何不可变如何实现的不可变)
    * [StringBuilder 和 StringBuffer 有什么区别？应用场景？](#stringbuilder-和-stringbuffer-有什么区别应用场景)
    * [ArrayList 和 LinkedList 的区别？](#arraylist-和-linkedlist-的区别)
    * [谈谈 final 在 Java 中的应用？](#谈谈-final-在-java-中的应用)
    * [HashMap 相关](#hashmap-相关)
        * [存储结构](#存储结构)
        * [为何是 2 倍扩容？](#为何是-2-倍扩容)
        * [如何进行冲突处理？](#如何进行冲突处理)
        * [多线程下的 HashMap](#多线程下的-hashmap)
    * [Error 和 Exception 有什么区别？](#error-和-exception-有什么区别)
    * [什么是多态？如何体现多态？](#什么是多态如何体现多态)
    * [NIO、BIO、AIO](#niobioaio)
    * [反射](#反射)
    * [深拷贝和浅拷贝](#深拷贝和浅拷贝)
* [二、JMM 与并发](#二jmm-与并发)
    * [什么是线程安全](#什么是线程安全)
    * [volatile 变量是什么？](#volatile-变量是什么)
    * [synchronized](#synchronized)
* [三、JVM](#三jvm)
    * [Xmx 和 Xms 如何使用？](#xmx-和-xms-如何使用)
    * [可达性分析算法](#可达性分析算法)
    * [垃圾回收算法](#垃圾回收算法)
* [四、框架](#四框架)
    * [对 Spring IoC 的理解？](#对-spring-ioc-的理解)
    * [Spring MVC 的请求流程](#spring-mvc-的请求流程)
* [五、数据库](#五数据库)
    * [索引](#索引)
        * [聚集索引与非聚集索引](#聚集索引与非聚集索引)
        * [索引失效](#索引失效)
    * [MySQL 引擎](#mysql-引擎)
    * [Redis](#redis)
        * [缓存机制](#缓存机制)
    * [乐观锁和悲观锁](#乐观锁和悲观锁)
    * [B 树和 B+ 树](#b-树和-b+-树)
* [六、算法](#六算法)
* [七、其他](#七其他)
* [操作系统](#操作系统)
    * [进程和线程的区别？](#进程和线程的区别)
* [网络](#网络)
    * [GET 和 POST 的区别？](#get-和-post-的区别)
    * [HTTP 1.0、1.1、2.0 的区别？](#http-101120-的区别)
<!-- GFM-TOC -->


# Java 常见面试题及答案

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

## ArrayList 和 LinkedList 的区别？

1. ArrayList 是实现了基于**动态数组**的数据结构，LinkedList 基于**双向链表**的数据结构。    
2. 对于随机访问 get 和 set，ArrayList 优于 LinkedList，因为 LinkedList 要移动指针。    
3. 对于新增和删除操作 add 和 remove，LinedList 比较占优势，因为 ArrayList 要移动数据。

## 谈谈 final 在 Java 中的应用？

final 可以作用在数据、方法和类上，分别起到不同的效果：

**1. 数据**

声明数据为常量，可以是编译时常量，也可以是在运行时被初始化后不能被改变的常量。

- 对于基本类型，final 使数值不变；
- **对于引用类型，final 使引用不变，也就不能引用其它对象，但是被引用的对象本身是可以修改的**。

```java
final int x = 1;
// x = 2;  // cannot assign value to final variable 'x'
final A y = new A();
y.a = 1;
```

**2. 方法**

声明方法不能被子类覆盖。

**private 方法隐式地被指定为 final**，如果在子类中定义的方法和基类中的一个 private 方法签名相同，此时子类的方法不是覆盖基类方法，而是在子类中定义了一个新的方法。

**3. 类**

声明类无法被继承。

## HashMap 相关

### 存储结构

### 为何是 2 倍扩容？

### 如何进行冲突处理？

### 多线程下的 HashMap

## Error 和 Exception 有什么区别？

Error 和 Exception 是 Java 异常体系中唯二的两个分支，它们均直接继承自 Throwable 类。

Error 是在正常情况下不应该出现的问题，由虚拟机抛出。对于 Error 程序员不需要进行捕获处理，一般也无法进行处理。常见的 Error 如 OOM（OutOfMemoryError），就是因为虚拟机内存不足造成的，我们在应用程序的层次无法对其进行捕获处理。

Exception 大致分为两大类，RuntimeException 和其他异常，如 IOException。对于 RuntimeException，一般是程序自身的问题，如访问数组越界、空指针……这些问题更应该从逻辑方面去解决，而不是去进行异常处理。所以 RuntimeException 和 Error 又被称为「非受查异常」（Unchecked Exception）。

而其他异常是程序运行过程中可以预料的异常，如 FileNotFoundException、EOFExcpetion 等等，程序必须对其进行捕获并进行相应的处理。如果不进行捕获，则必须声明可能抛出的受查异常，让异常「冒泡」。没有被处理的异常会沿着调用链传递下去，如果最终都没有一个方法对其进行处理，那么异常会由虚拟机处理，虚拟机就「死」给你看了。

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

## NIO、BIO、AIO

## 反射

**什么是反射**

反射机制是 Java 语言提供的一种基础功能，通过反射赋予了程序内省（introspect，即在运行时获取程序类、对象、方法等等构建信息）的能力。

反射主要提供了以下的几种功能：

- 在运行时判断任意一个对象所属的类。
- 在运行时构造任意一个类的对象。
- 在运行时判断任意一个类所具有的成员变量和方法。
- 在运行时调用任意一个对象的方法

**反射的使用场景**

例如经典的 JDBC 应用，对于不同的数据库需要使用不同的连接。

```java
Connection conn = new MySQLConnection();
```

数据库被更换为 Oracle 后，需要修改代码、重新编译……

```java
Connection conn = new OracleConnection();
```

而有了反射，我们可以将数据库连接名写在配置文件中，通过反射动态的调用数据库连接类：

```java
Connection conn = Class.forName("conn").newInstance();
```

另外，最常使用反射的就是各类基础框架，比如 Spring、Hibernate 就大量使用了反射。框架是给调用者提供服务的，但框架怎么知道调用者的类信息、方法信息呢？通过反射。反射同样是动态代理、AOP 等的基础。

## 深拷贝和浅拷贝

- 浅拷贝：对于基本数据类型，拷贝它的值，对于引用数据类型（对象），拷贝它的引用
- 深拷贝：对于基本数据类型和引用数据类型都是拷贝值

**如何实现深拷贝**

- 序列化：将一个对象序列化，再反序列化回来，得到的就是一个全新的对象
- 覆盖实现 clone() 方法：在自定义的 clone() 方法中对引用数据类型在进行一次拷贝即可

# 二、JMM 与并发

## 什么是线程安全

> 当多个线程访问一个对象时，如果不用考虑这些线程在运行时环境下的调度和交替执行，也不需要额外的同步，或者在调用方进行任何其他的协调操作，调用这个对象的行为都可以获得正确的结果，那么这个对象是线程安全的。

以上是《Java 并发编程实战》一书中作者给出的关于线程安全的定义。

## volatile 变量是什么？

一旦一个共享变量（类的成员变量、类的静态成员变量）被 volatile 修饰之后，就具备了两层语义：

1. 保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的。
2. 禁止进行指令重排序。
3. **volatile**变量不保证原子性

## synchronized

synchronized 语句需要一个对象的引用；随后会尝试在该对象的管程上执行 lock 动作，如果 lock 动作未能成功完成，将一直等待。当 lock 动作执行成功，就会运行 synchronized 语句块中的代码。一旦语句块中的代码执行结束，不管是正常还是异常结束，都会在之前执行 lock 动作的那个管程上自动执行一个 unlock 动作。

如果是实例方法，synchronized 锁的是调用该方法的实例（即方法体执行期间的 this）相关联的管程。如果是静态方法，锁的是定义该方法的类所对应的 Class 对象。

# 三、JVM

## Xmx 和 Xms 如何使用？

Xmx 和 Xms 是 Java 虚拟机启动时的可选参数。

Xmx 指定 Java 虚拟机最大可分配内存，超出此内存将会产生 OutOfMemoryError 异常。Xmx 通常具有默认值 256 MB。 

Xms 指定 Java 虚拟机初始化时占用的内存大小，此项一般没有默认值。

## 可达性分析算法

Java 中的判断对象生存状态的算法是可达性分析。它会通过一系列的称为「**GC Roots**」的对象为起点，从这些节点开始向下搜索。搜索走过的路径称为引用链（Reference Chain），当一个对象到 GC Roots 没有任何引用时，就表明对象已死。

Java 中可以充当 GC Roots 的对象包括以下几种：

- 虚拟机栈（栈帧中的本地变量表）中引用的对象
- 方法区中类静态属性引用的对象
- 方法区中常量引用的对象
- 本地方法栈中 JNI 引用的对象

## 垃圾回收算法

# 四、框架

## 对 Spring IoC 的理解？

## Spring MVC 的请求流程

用户在 Web 浏览器中点击 URL 或者提交表单的时候，就开始了请求的工作。

请求的第一站是 DispatcherServlet。DispatcherServlet 在此充当一个前端控制器（front controller）的角色。所有的请求都经由 DispatcherServlet，它将请求转发给具体的控制器来处理。

控制器是一个用于处理请求的 Spring 组件，通常存在多个控制器，所以 DispatcherServlet 需要知道将请求发送给哪个控制器。DispatcherServlet 会去查询处理器映射（handler mapping），来确定下一站在哪。处理器映射会根据请求携带的 URL 来决定请求应该交给哪个控制器来处理。

找到了合适的控制器后，DispatcherServlet 会将请求发送给控制器。控制器完成处理后，通常会产生一些信息，这些信息被称为模型（model）。信息的可视化处理需要发送给一个视图（view），通常是 JSP。

控制器将模型数据打包，并标识出用于渲染输出的视图名，然后将其发送给 DispatcherServlet。DispatcherServlet 接收到后，使用视图解析器（view resolver）将逻辑的视图名匹配为一个特定的视图实现。最后，视图将模型数据渲染，输出，并返回给客户端。

![](assets/201804161409_586.jpg)

# 五、数据库

## 索引

### 聚集索引与非聚集索引

### 索引失效

## MySQL 引擎

## Redis

### 缓存机制

## 乐观锁和悲观锁

## B 树和 B+ 树

# 六、算法

# 七、其他

# 操作系统

## 进程和线程的区别？

**进程是资源分配的最小单位，线程是 CPU 调度的最小单位。**线程是不拥有资源的（或者说只拥有极少的保证自己足以运行的资源），线程可以访问属于进程的资源。

线程是进程的子集，一个进程可以拥有多个线程。同一进程下的线程资源共享，而不同的进程间如果想要共享数据只能通过进程间通信（IPC）来实现。

一个运行中的程序通常对应一个进程，但通常对应多个线程。如我们登录 QQ 后，可以一边给朋友发信息一边接收朋友的信息，如果只有一个线程，想接收新的消息就只能等你的消息发送完毕后才行。多线程使得计算机的多任务并发处理更加方便快捷。

最后，开销方面，线程间切换的开销远远小于进程切换的开销。

# 网络

## GET 和 POST 的区别？

- GET 也可以用来提交信息，但提交后信息的内容会显示在 URL 后缀上，不用来提交敏感数据
- POST 有一个消息体，GET 只有请求头
- GET 幂等（还有 PUT、HEAD)，POST 不幂等（幂等，反复做一件事情而没有副作用）

## HTTP 1.0、1.1、2.0 的区别？