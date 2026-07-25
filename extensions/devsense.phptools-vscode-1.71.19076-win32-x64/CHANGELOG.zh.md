## 1.71.19076 (2026年7月16日)

### 代码操作

编辑器现在为带有 `#[Deprecated( ..., replacement: ... )]` 属性注释的过时符号提供快速修复。

### 次要改进

- 如果存在声明为 `private` 的相同属性，则会考虑 `@property` 定义。[#1055](https://github.com/DEVSENSE/phptools-docs/issues/1055)
- 识别并考虑 PHPStan 提供的 PHPDoc 类型提示中数组偏移量的语法格式，例如 `TArray['key']`。然而，在泛型情况下的类型推断仍然受限。[#632](https://github.com/DEVSENSE/phptools-docs/issues/632)
- 对间接函数调用的参数进行验证和提供参数内嵌提示。
- 对 `instanceof` 表达式中未知类名提供快速修复。
- 在代码补全中添加了一些常用的片段。
- 实现接口的代码操作（_实现抽象成员_）也实现了属性。

## 1.71.19014 (2026年6月22日)


### 次要改进

- 检查有效回调函数时，支持除了函数名之外，还可以是 `string`。 [#1053](https://github.com/DEVSENSE/phptools-docs/issues/1053)
- 检查属性设置的可见性。 [#2589](https://community.devsense.com/d/2589)
- 对 `__construct` 的引用代码透镜同样统计对 `new` 的引用（与_查找所有引用_功能行为一致）。 [#1050-comment](https://github.com/DEVSENSE/phptools-docs/issues/1050#issuecomment-4742244665)
- 修复了 HEREDOC 字符串中包含转义换行符的错误警告。 [#2577](https://community.devsense.com/d/2577), [#1053](https://github.com/DEVSENSE/phptools-docs/issues/1053), [#2591](https://community.devsense.com/d/2591)。此更新还添加了 HEREDOC 文本中的精确错误报告，因此带有错误缩进的确切行会被标下划线。

## 1.71.18989（2026年6月16日）



### IntelliSense

- 添加了数组类型可调用语法中的方法名称代码补全。
- _查找所有引用_ 到字符串文字列出用户代码中该文本的所有出现。
- _查找所有引用_ 到已知的字符串值（例如，WordPress钩子名称）。[#2588](https://community.devsense.com/d/2588)
- 数组类型可调用语法中函数的工具提示。
- 字符串类型和数组类型可调用的函数名称验证和导航。

  ![Array Callback Intelligence](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/array-callback-intelligence.png)

  **类数组回调**和**类字符串回调**进行了验证，获得上下文补全、导航、语义高亮、重命名重构，以及显示相关函数详细信息的工具提示。

### WordPress

- _WordPress_ 存根中的函数和类具有指向文档的正确链接。[#1039](https://github.com/DEVSENSE/phptools-docs/issues/1039)
- _导航_ 至WordPress钩子调用。
- _查找所有引用_ 到WordPress钩子。
- 工具提示表明字符串值的类型（例如，`(WordPress Hook) 'wp_head'`）。

![WordPress Hooks](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/frameworks/img/wp-hook-references.png)

### PHP 手册

整个多语言PHP手册已更新，包含新的PHP存根、额外的翻译和以前未记录的PHP功能和类。这些更新提高了代码智能、代码分析和代码操作。

![Chinese PHP Manual](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/php-manual-chinese.png)

### 小幅改进

- 如果禁用了代码操作，则不显示重构提示。[#1038](https://github.com/DEVSENSE/phptools-docs/issues/1038)
- `is_null()` 代码操作在必要时添加括号。
- _Laravel_：改进从分组声明中的`Route`定义导航到控制器的动作。
- 返回未初始化变量的函数被视为返回 `mixed`。[#1045](https://github.com/DEVSENSE/phptools-docs/issues/1045)
- 不报告lambda的 `use()` 中不明全局变量。[#1044](https://github.com/DEVSENSE/phptools-docs/issues/1044)
- 尊重暂定类型，并修复类覆盖中的错误警告。[#1043](https://github.com/DEVSENSE/phptools-docs/issues/1043)
- 改进了 `BcMath` 支持。[#2559](https://community.devsense.com/d/2559)
- _大纲_ 视图中的 `namespace` 符号根据 `"outline.showNamespaces"` 设置显示。[#2578](https://community.devsense.com/d/2578)

  ![WordPress Hooks](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/outline-with-namespace.png)

## 1.70.18915 (2026年5月27日)




### 智能感知与诊断

- 类型推断遵循由 `BcMath\Number` 重载的算术运算符。[#2559](https://community.devsense.com/d/2559)
- 识别不带错误代码的独立 `@disregard` 标签（`@suppress` 的别名）。标签在语句或函数上方时，将导致编辑器忽略所有警告。
- 改进了注释有通用模板类型的变量后的智能感知。[#2565](https://community.devsense.com/d/2565)
- 在数组访问和 foreach 循环中的类型推断尊重歧义。[#2522](https://community.devsense.com/d/2522)
- 对应于未使用的 `$_` 的警告默认被忽略，因为 `$_` 被视为占位符变量。[#2570/2](https://community.devsense.com/d/2570-at-suppress-is-not-working-may-2026/2)
- 修正了对 `@require-extends` 的检查。[#2572](https://community.devsense.com/d/2572)

### 用户界面

- VSCode 识别 `"hostname"` `launch.json` 属性。[#2551/3](https://community.devsense.com/d/2551/3)
- 如果 VSCode 的显示语言是中文，则新的更新日志将以中文显示。

## 1.70.18851 (May 13, 2026)





### 改进

- 现在支持 `"numeric-string"` 类型；从数字字符串进行的隐式转换不再生成不必要的警告。
- 各种控制流分析的清理和稳定性改进。

### PHPDoc

- 解析嵌套的 PHPDoc 标签更加宽松，提升了 PHPDoc 解析的稳健性。
- 修复了 `@global` 出现的匹配。
- 修复了 PHPDoc 标签中的类型名称代码补全。[#892 (comment)](https://github.com/DEVSENSE/phptools-docs/issues/892#issuecomment-4422799460)

### IntelliSense

- `$GLOBALS['NAME']` 在鼠标悬停和重构功能中现在得到更具体的处理。
- 修复了当数组具有多种元素类型时对动态属性的类型推断。

### WordPress

- 增加了对更多非标准 WordPress 类型语法的兼容性。
- 扩展了对结构化 WordPress 类型语法规范的支持。

## 1.70.18840 (2026年5月9日)





### 小幅改进

- 更好地识别Laravel路由，即使在组中定义。
- 非Laravel项目的性能和内存优化。
- 改进了对泛型模板类型的处理；当它们未绑定时传递给基类范围。[#2501](https://community.devsense.com/d/2501), [#2504](https://community.devsense.com/d/2504)
- 更新了精选建议AI模型。
- 更符合WordPress惯例，减少错误报告。
- 在IntelliSense中新增了添加存根的代码操作（`php.stubs`设置）。这解决了PHP手册中定义的未知函数或未知类名的问题。

### 中文本地化

扩展UI和IntelliSense显示为中文。如果您的VSCode显示语言设置为`zh-cn`，则会自动设置。

## 1.70.18740（2026年4月7日）




### 新功能

- 为带默认值的不正确变长参数添加了诊断。[#1025](https://github.com/DEVSENSE/phptools-docs/issues/1025)
- 属性名称的补全仅列出有效的属性类（具有 `#[Attribute]` 的类）。[#2511](https://community.devsense.com/d/2511)
- 更多的 Laravel 控制器补全。[#2502](https://community.devsense.com/d/2502)
- PHP 手册浏览器显示属性（从 PHP 手册导航到符号，例如 `Override`。）
- 日语用户界面本地化。
- 泛型模板参数适用于嵌套的本地函数和 lambda 函数。

### 修复

- 修复了 `View` 类型后的 Livewire IntelliSense。
- 文件末尾紧接 `<?php` 后的误报语法错误。[#1026](https://github.com/DEVSENSE/phptools-docs/issues/1026)
- 修正了 `php.format.rules.keepControlStatementsOnOneLine` 不正确地删除方法体前空行的问题。[#2542](https://community.devsense.com/d/2542-formatting-bug)

## 1.69.18673 (2026年3月26日)





### 星标建议

最可能的成员补全现在会用星标 ★ 标记，并显示在列表顶部。这样可以帮助您更快地找到正确的项目，减少输入量。

![starred suggestions](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/editor/imgs/starred-completion.png)

如果您继续输入，什么都不会改变。此功能不会妨碍您的操作，且能自然融入您的常规工作流程。

> 可以使用 `"php.completion.starredSuggestions"` 设置来禁用或启用星标建议。  
> 注意：该功能不支持 _Alpine Linux_ (`musl`)。

### 新功能

- 添加参数类型提示的代码操作。
- Livewire 框架定义的方法已添加至 IntelliSense (`View::layout()`, `View::title()`)。[#2530](https://community.devsense.com/d/2530)

### 次要更改

- `Premium` 用户在欢迎屏幕上不再看到 "Buy" 按钮。
- Alpine/musl 再次有专用安装程序。[#1020](https://github.com/DEVSENSE/phptools-docs/issues/1020)
- `PHP0412` (_undefined property_) 警告现在在属性赋值时报告，而非后续读取时。这与其他代码分析工具更加一致，并且与相应的工具提示结合时更具合理性。如果属性在 `@property` 文档块中指定，或存在魔术方法 `__get`/`__set`，则不报告警告。

### 修复和改进

- 修复解析 _Laravel_ 路由定义中的控制器方法。[#2502/7](https://community.devsense.com/d/2502/7)
- 在编辑文件时，工作区中的问题会延迟重新分析。
- CSS 规则及相关的 Blade 语法修复。[#1023](https://github.com/DEVSENSE/phptools-docs/issues/1023)
- 修复缺少参数的函数重写错误，快速纠正不会移除右括号 `)`。
- 工作区加载时间优化。

## 1.68.18590 (2026年3月11日)





### 功能

- PHP 8.5 `(void)` 转换。
- 类型层次结构支持。
- 自定义 WordPress 动作和过滤器代码补全。
- PHP 开始标签的代码补全（'<?php' 等）。

### 修复

- 修复了 `php.format.rules.alignConsecutiveAssignments` 格式化问题，这导致在 case 项目内无法直接对齐。
- 修复了在存在深度递归时 lambda `use` 中未使用变量的检查。[#1010](https://github.com/DEVSENSE/phptools-docs/issues/1010)
- 修复了从不同 trait `use` 块的 trait 适配问题。[#1012](https://github.com/DEVSENSE/phptools-docs/issues/1012)
- 修复了来自 composer 包的声明的弃用检查。

## 1.67.18520 (Feb 17, 2026)





### 修复

- 修复了字符串插值中的解析器，如 `"{$a}b"`。
- 修复了在先前错误恢复后的错误语法错误。
- 修复了带有结尾逗号的 `match` 分支的格式。[#1007](https://github.com/DEVSENSE/phptools-docs/issues/1007)

### 次要更改

- 为与字符串插值不同的字符串连接提供代码操作。[#970](https://github.com/DEVSENSE/phptools-docs/issues/970)

## 1.67.18502 (2026年2月13日)





### 修复

- 基础方法返回`static`时的方法覆盖诊断。[#932](https://github.com/DEVSENSE/phptools-docs/issues/932)
- 特殊lambda函数（例如Pest PHP测试）中的方法可见性。[#1006](https://github.com/DEVSENSE/phptools-docs/issues/1006)
- 修复了多行函数调用中命名参数缺少缩进的问题。[#2510](https://community.devsense.com/d/2510)
- 修复了使用`{$var}`进行字符串插值后的签名帮助。[#4](https://github.com/DEVSENSE/php4vs/issues/4)

## 1.67.18497 (Feb 11, 2026)





### Laravel

- `Storage::fake('')` 已处理，因此接下来的 `Storage::disk('')` 被识别为返回带有 `assert` 方法的 `FileSystemAdapter`。
- `\Pest\Laravel\actingAs()` 返回更具体的 `TestCase` 类，包括 `Architectable` 和 `Browsable` traits。

### 次要功能

- 新的 `URI` 扩展在旧版本 PHP 中使用时，会被正确报告为从 PHP 8.5 起可用。
- **Pest 的高阶测试**代码补全，包括 `Browsable` 和 `Architectable` traits。
- 尊重带有可选参数的闭包/可调用的 PHPDoc 注释。[#1000](https://github.com/DEVSENSE/phptools-docs/issues/1000)
- 代码操作：`Remove Unnecessary Spread`。
- 代码操作：用 `clone with` 替换 `clone`。
- 不显示变长参数的内嵌提示（没有意义）。
- 诊断 _TraitMethodConflict_ `PHP2447`。[#1002](https://github.com/DEVSENSE/phptools-docs/issues/1002)
- 错误容忍解析器的初步实现。
- 在函数调用中，如果展开运算符的数组键与已提供的参数不冲突，则进行检查。

### 修复

- 避免对错误的 NEON 文件（PHPStan 配置）发出警告，如果文件实际上是 `.php` 文件。`.php` PHPStan 配置不受支持。
- 当鼠标悬停和导航在 `"string"` 值上时，不会总是导航到同名的全局函数——只有在使用字符串的参数为 `callable` 时才会导航。
- 修复在名为 `Match` 的类中出现的不必要空行。[#984](https://github.com/DEVSENSE/phptools-docs/issues/984)
- 修复 Laravel 的 `enum_value()` 返回类型错误。
- 修复语法错误的错误消息。
- 修复对 `interface` 上 `@extends` 的检查。[#2513](https://community.devsense.com/d/2513)
- 遵循匿名函数的可选参数。
- 通过 `self::` 在 `trait` 中引用私有 `const`。[#1004](https://github.com/DEVSENSE/phptools-docs/issues/1004)

## 1.66.18408 (2026年1月29日)





### 次要特性

#### 参数验证

为闭包和间接函数调用添加了参数验证。  
  [#2503](https://community.devsense.com/d/2503)

  ![check closure call](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/cfg-closure-args.png)

#### 重构、引用和导航

改进了在特定代码模式中的 `"string"` 值的重构、引用和导航，例如  
  `new ReflectionMethod(FQN::class, "HERE");`。  
  [#2502](https://community.devsense.com/d/2502)

  ![resolve symbols](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/editor/imgs/resolve-string-symbols.png)

#### Laravel 支持

添加了对 Laravel 控制器动作方法的补全支持。  
  [#2502](https://community.devsense.com/d/2502)

  ![laravel controller method completion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/editor/imgs/complete-controller-method.png)

#### 编辑器洞察与导航

增强了鼠标悬停和导航功能，提供了更详细的方法结果，使用与代码分析相同的逻辑。  
  这提高了对生成的存根、助手和重载方法的可见性，并使编辑器内部实际看到的内容更加清晰。

  ![hover all methods](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/editor/imgs/hover-all-method-stubs.png)

### 修复

- 修复了在 `@var` 注解中 `Closure` 类型名称的语义高亮和未使用的 `use` 检查。
- 修复了 IntelliSense 中缺少的 Symfony polyfills 并避免了使用 polyfills 时的错误弃用警告。
- 修复了 `@formatter:off` 行为，以正确保留原始的空白和大括号位置。

## 1.66.1837 (2026年1月26日)




### 修复

- 修复当存在有缺陷的 `_laravel_ide` 存根时的方法解析。[#990](https://github.com/DEVSENSE/phptools-docs/issues/990)
- 改进对静态/非静态方法调用的方法解析。
- 改进Laravel模型的IntelliSense - 正确展示和解析来自查询构建器的静态辅助函数。
- 修复基于方法断言的 Str::startswith() 类型推断。[#2498](https://community.devsense.com/d/2498)

## 1.66.18374 (2026年1月24日)





### 调试

- 添加了对函数返回值的支持。不再需要临时变量来检查函数结果。在“变量”窗格中捕获并显示返回值，并在“Step Out”后清楚地标识源函数（例如，`strtoupper()`）。
- 改进了在 launch.json 中对 `XdebugSettings` 的支持。现在可以可靠地覆盖任何 DBGp 功能（如 `max_data`、`max_children` 或 `max_depth`）。[#2450](https://community.devsense.com/d/2450-xdebug-settings-cannot-be-changed)

### 次要功能

- 代码补全中的 `@pure`（以及 `@phpstan-pure`、`@psalm-pure`）标签。请注意，此功能尚未被代码分析使用。
- 内存使用优化。
- 简化使用字符串插值的字符串连接的代码操作处理更多可能的情况。
- 尊重 PHP `7.x` 和 `8.x` 之间的小语法差异，即命名空间名称中的半保留标记。当[更改 PHP 版本](https://docs.devsense.com/vscode/php-version/#choosing-php-version)时，打开的 PHP 文档内的语法也会重新评估。修复了 [#963](https://github.com/DEVSENSE/phptools-docs/issues/963) 和类似问题。
- `PHP 8.5 **URI**` 扩展已添加到工作区存根列表中（默认未启用 - 请参阅“Workspace Stubs”命令）。

### 修复

- 带有位于 `vendor` 目录之外的非标准 `installPath` 的 Composer 包不会被重复索引和缓存；这修复了 IntelliSense 中的双重出现、不必要的内存使用，以及不必要的初始 CPU 使用。这也改善了代码流分析和受影响项目中的整体编辑器体验（如 _Drupal_）。
- 对 vararg 参数的数组类型注释进行了处理。[#2489](https://community.devsense.com/d/2489)
- 对于未知类型的类成员，语义高亮工作，即 `$unknown->member`。
- 在 `.blade.php` 中，编辑器列出了“后端代码”的代码操作（由模板引擎生成的代码）；这些代码操作会分散注意力，没有意义，并且会生成无效的代码更改。[#985(2)](https://github.com/DEVSENSE/phptools-docs/issues/985)
- 修复了文档注释中的语义颜色，未在文档编辑或保存时进行着色。
- 改进了使用 `true` 和 `false` 常量的条件 `@return` 注释。
- 修复了在工作区中有无效的 `class_alias()` 或 `constant()` 时缺失的代码补全。
- 修复了 NEON 文件解析。[#992](https://github.com/DEVSENSE/phptools-docs/issues/992)
- 修复了 `protected` 函数可见性检查的问题，当方法声明在作用域外但其原型不存在时。[#2496](https://community.devsense.com/d/2496)
- 修复了 `try`/`catch` 代码流分析的问题，其中 `goto` 的标签位于 `finally` 内。
- 修复了引入错误的 `define()` 或错误的 `class_alias()` 函数时出现无效类名或常量名的代码补全。
- 修复了设置 `"php.format.exclude"`，使其支持工作区相对路径。[2499](https://community.devsense.com/d/2499)
- 修复了 `ArrayObject::exchangeArray()` 参数签名。[#2494](https://community.devsense.com/d/2494)
- 在联合类型中实现了代码补全和鼠标悬停。[#2492](https://community.devsense.com/d/2492)

## 1.65.18327 (Jan 14, 2026)





### 新功能

- 支持PHP 8.5的新语法和可选参数中将`clone`作为函数使用。 [#2478](https://community.devsense.com/d/2478)
- 支持PHP 8.0的可解引用字符串语法。 [#2479](https://community.devsense.com/d/2479)
- 为类属性钩子启用了CodeLens。 [#2476](https://community.devsense.com/d/2476)
- 新增`@return`条件注释，允许比较常量和参数值（_数字_、_字符串_和_`null`_），例如
  ```php
  /** @return ( $name == null ? false : int ) */
  function foo( $name ) { return $name === null ? false : strlen($name); }
  ```
  或
  ```php
  /** @return ( PHP_MAJOR_VERSION >= 8 ? string[] : array|false ) */
  function foo() { ... }
  ```
  可能的操作符包括`is`（与之前的类型比较相同），以及新增的`==`、`<=`、`>=`、`<`、`>`。
- `explode()`函数使用PHP版本特定的返回类型注释显示（在工具提示中、通过类型分析以及在生成的文档中）。 [#860](https://github.com/DEVSENSE/phptools-docs/issues/860)
- 为接口和枚举添加特定的颜色（如果用户的主题支持）。
- 为属性钩子中的类型提示中的类型名称添加颜色。

### 修复

- 修复了枚举案例的CodeLens。 [#2482](https://community.devsense.com/d/2482)
- 在诊断中尊重生成的`_ide_helper`、`_laravel_idea`和`_laravel_ide`。 [#974](https://github.com/DEVSENSE/phptools-docs/issues/974), [#2486](https://community.devsense.com/d/2486)
- 修复了与新作用域绑定的`Closure`中关于错误成员可见性的错误警告。
- 导航和鼠标悬停在当前作用域中不可见的类属性也能工作。
- 修复了命名空间名称中`Echo`的语法错误。
- 修复了如果有`phpstan/php-8-stubs` composer包则所有的IntelliSense信息都变得模糊（速度较慢且不够精确）的问题。 [#2481](https://community.devsense.com/d/2481)
- 针对罕见的语言服务器崩溃进行可能的修复。 [#979](https://github.com/DEVSENSE/phptools-docs/issues/979)

### 未使用的类成员高亮显示

如果没有直接的用法，未使用的类方法、常量和属性现在会被变暗显示。

## 1.64.18270 (Dec 30, 2025)





### 优化

我们在编辑器中引入了重要的**解析器优化**。PHP 编辑器现在可以跟踪增量变化，并惰性解析代码，当编辑不重要时完全跳过解析。这将打字时的 CPU 使用量减少了大约 90%，在较大的 PHP 文件中尤其明显。

此外，**初始索引**也进行了优化。不过，建议您将工作区文件夹排除在杀毒软件扫描之外，以获得更好的性能。

最后，CodeLens 支持也有所改进。它现在使用的 CPU 显著减少，主要是因为其底层算法已被重新实现。

### 修复

* 修复 `.editorconfig` 文件内的补全。建议包括可能的格式规则和代码操作配置。
* 改进了 `is_numeric()` 类型推断。
* 改进了 CodeIgniter 3 项目中的库支持。
* 修复了 PHPDoc 中意外的 `!` 的诊断位置。
* 解决了多个带有 `empty-string` 类型提示的负 `@phpstan-assert-if-***` 注释的问题。[#967](https://github.com/DEVSENSE/phptools-docs/issues/967)
* 如果已抑制相应的诊断，不要使代码变暗或删除线。
* 当类层次结构不完全已知（存在未知基类）时，在 `catch` 子句中不报告错误的类。
* 修复了访问已修改的结构数组类型的数组项时的错误警告。[#969](https://github.com/DEVSENSE/phptools-docs/issues/969)
* 修复了在启用 `Keep*OnOneLine` 设置时的空行处理。[#964](https://github.com/DEVSENSE/phptools-docs/issues/964)
* 更名时，无效的新标识符现在会导致带有详细信息的弹出消息。
* 正确地从特质适配块中找到方法的引用，包括那些被适配块重命名的方法。
* 修复了对 `ReflectionMethod::__construct()` 的错误弃用建议。

### 次要特性

* `@suppress`（或 `@suppresswarnings`）标签识别选定的 `PHPMD` 代码。
* `empty-string` 类型提示被识别。
* 针对总是为假的严格比较的诊断。[#971](https://github.com/DEVSENSE/phptools-docs/issues/971)
* 对传统构造函数的弃用检查更加详细。

## 1.63.18172 (Dec 3, 2025)





### 次要功能

- 支持内联 PestPHP 测试用例运行器。[@MrPunyapal](https://x.com/MrPunyapal/status/1994339061956329731)
- 为建议的参数字符串值提供代码补全。
- 支持 `@psalm-assert-if-true`，`@psalm-assert-if-false`。
- 支持 `@phpstan-assert` 或 `psalm-assert`，类型提示以 `=` 前缀，用于 PHPUnit 的 `assertInstanceOf()`。
- 遵循 `@phpstan-ignore-line`。

### 修复

- 使用成员字段或匿名函数在常量表达式中引发的错误。[#955](https://github.com/DEVSENSE/phptools-docs/issues/955)，[#958](https://github.com/DEVSENSE/phptools-docs/issues/958)
- 在 `and`，`or` 条件中显示无效的冗余括号提示。[#2467](https://community.devsense.com/d/2467)
- 修复当存在无效的 `@dataProvider` 注解时语言服务器崩溃的问题。

## 1.63.18152 (2025年11月27日)





### 次要功能

- 测试运行中，有些在 `phpunit.xml` 配置中被排除但在测试视图中被选择/过滤的测试组。这样可以使用 `<groups><exclude><group>...` XML 配置排除大型/缓慢的测试，这样当运行所有测试时，不会默认运行这些测试。如果使用过滤框选择或过滤了那些被排除的测试，这种排除将被覆盖。 [#2426](https://community.devsense.com/d/2426-test-explorer-does-not-filter-by-at-group/12)
- `/vendor/**` 文件夹中的问题（包括像 `composer` 这样的特殊子文件夹）现在根本不会被列出，除非在编辑器中打开 `vendor` 文件夹下的文件。
- `is_numeric` 的类型缩小。 [#2436](https://community.devsense.com/d/2436)
- 添加了 `php-amqp` 声明文件。
- 设置 `files.exclude`、`php.files.exclude`、`search.exclude`、`php.problems.exclude` 支持带有组、范围、否定和特殊字符的 glob 模式，这些字符被括在 `[`、`]` 中。 [#945](https://github.com/DEVSENSE/phptools-docs/issues/945)
- 添加了命令 `PHP Tools: Quick Settings ...` 来访问常用的 PHP 编辑器设置。
- 更新了多语言 PHP 手册。
- 暗淡无用的私有类函数。 [#800](https://community.devsense.com/d/800)
- 快速重构，以用数组展开替换 `array_merge`。
- 快速重构，以在 PHP >= 8.4 中清除 `new` 周围不必要的 `()`。
- 快速重构，以从匿名函数创建新的 callable 语法。
- 补全 `compact()` 函数中的变量名。
- 对属性和各种初始化器中的常量表达式 (`PHP2446`) 进行诊断。在 [#2458](https://community.devsense.com/d/2458)、[#949](https://github.com/DEVSENSE/phptools-docs/issues/949) 中查看。
- 改进了复杂层次结构中 `enum` 定义的重写检查。 [#2460](https://community.devsense.com/d/2460)
- 对于类型化属性中的联合类型和交集类型的未知类型检查。 [#2461](https://community.devsense.com/d/2461)

### 修复

- 修复了在完成带参数或括号的函数时自动关闭 `)` 错误。 [#947](https://github.com/DEVSENSE/phptools-docs/issues/947)
- 修复了属性内部的快速修复。
- 修复了将代码操作转换为包含对象操作符 `->` 的箭头函数。
- 如果文件名不是有效的类名标识符，则不建议进行 PSR-4 类名修正。
- 在常量表达式中不建议使用箭头 `fn`。 [#949](https://github.com/DEVSENSE/phptools-docs/issues/949)
- 未使用的函数声明不会报告 `__construct` 和其他魔术方法。[#950](https://github.com/DEVSENSE/phptools-docs/issues/950)
- 修复了 `@phpstan-assert` 影响的代码流中的表达式多于其应有的情况。 [#2459](https://community.devsense.com/d/2459)

### 重大变更

- 默认情况下，设置 `"php.completion.intelliPHP.preSelect"` 为 `false`。尽管[此功能非常棒](https://docs.devsense.com/vscode/editor/intelliphp/#pre-selecting-the-item-in-the-completion-list)，但它可能会使代码完成速度减慢50 - 250 毫秒。

## 1.62.18097 (2025年11月12日)




### 自动导入与分组

新增功能，自动导入遵循现有的 `use` 分组，因此导入的限定名称被添加到组中。

新的设置允许在合适的情况下创建新的 `use` 分组。

```json
"php.completion.autoimport": "auto-import-grouped"
```

![auto-import grouped](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/editor/imgs/vsc-autoimport-group.gif)

### 未优化的特殊编译器函数诊断

[#2438](https://community.devsense.com/d/2438): 如果编译器优化的函数没有在当前范围内导入，编译器无法将其翻译为更高效的OP代码。新增诊断 `PHP6616` 用以标记此类函数调用。

![native function invocation](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/native-function-invocation-example.png)

默认情况下，此类问题标记不太显著，并且不会列在VSCode问题窗口中。以下配置允许它被更显著地突出显示，甚至在 _文件保存_ 时自动修复，或通过触发VSCode的“自动修复...”命令进行修复。

`.editorconfig`
```ini
[*.php]
php_diagnostic_php6616=autofix
```

在我们的[博客文章 blog.devsense.com](https://blog.devsense.com/2025/optimize-native-function-invocation/)上阅读更多。

### 小功能

- 注解 `@phpstan-assert` 和 `@psalm-assert` 在 `vendor` 文件夹中均得到支持。
- 改进的**CI3**支持；从加载的库中为您的 `CI_Controller` 添加动态属性。
- 在函数调用内定义数组时的数组键自动完成，支持结构化数组参数提示 [#942](https://github.com/DEVSENSE/phptools-docs/issues/942)。
- 改进了_不必要的括号_提示，遵循 `and` 和 `=` 操作符的优先级，增加了对 `||`、`&&`、赋值、`if` 和其他二元操作符的更多提示 [#2444](https://community.devsense.com/d/2444)。

### 修复

- 修复了在composer包中的一个方法返回 `self` 但仅在基础接口中进行类型注解时的类型推断错误。[#941](https://github.com/DEVSENSE/phptools-docs/issues/941)
- 修复：对齐连续赋值功能现在在可调用（闭包和匿名函数）内部正确工作。[#2442](https://community.devsense.com/d/2442-align-consecutive-assignments)
- 修复在刀片组件视图和刀片组件类之间切换的问题（[文档](https://docs.devsense.com/vscode/frameworks/laravel/#switch-between-blade-view-and-class)）。[#2443](https://community.devsense.com/d/2443)

## 1.62.18042 (2025年10月30日)





### 新功能

- 支持 **PHPUnit 组**，因此测试可以在测试面板中按组名称进行过滤。
- 改进了在类型检查时对错误分支的类型推断。
- 改进了利用 `class-string` 类型的类型推断。
- 命名参数嵌入提示的鼠标工具提示。
- 连续赋值对齐现在支持不同类型的赋值语句格式化（例如，=、+=、??=，等）[#2432](https://community.devsense.com/d/2432)

## CodeIgniter 3

轻量、流行的 **CodeIgniter 3** 框架有其独特的特性和约定，许多 PHP 编辑器可能无法正确处理。Visual Studio Code 的 PHP Tools 现在内置支持 CodeIgniter 3。这个支持将在即将更新中进一步增强。

![CI3 completion](https://docs.devsense.com/vscode/frameworks/img/ci3-view-completion.png)

在此版本中你可以看到：
- 模型名称的自动补全。
- 视图名称的自动补全。
- 控制器中加载类的自动补全。

特别感谢在 [#677](https://github.com/DEVSENSE/phptools-docs/issues/677) 中的贡献。  
请参见更多信息：[docs.devsense.com](https://docs.devsense.com/vscode/frameworks/codeigniter3/)。

### 修复

- 实现接口的支持 `enum` 正确解析为 `BackedEnum` [#930](https://github.com/DEVSENSE/phptools-docs/issues/930)。
- 未在命名空间中声明的测试用例结果未被记录 [#936](https://github.com/DEVSENSE/phptools-docs/issues/936)。
- 修复了未基于 Laravel/Symfony 框架的 `App\Models\` 类的错误类型推断。

## 1.62.17969 (2025年10月9日)





### 测试代码覆盖率

我们引入了对测试[_代码覆盖率_](https://docs.devsense.com/vscode/test-explorer/#code-coverage)的支持。立即试用，导航到_测试_面板，然后点击_运行带覆盖率的测试_按钮。代码覆盖率将会显示在_测试_面板、_资源管理器_面板中，并直接显示在您的代码中。

![code coverage button](https://docs.devsense.com/vscode/imgs/code-coverage-start-button.png)

![code coverage](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/code-coverage-results-explorer.png)

![code coverage](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/code-coverage-visual.png)

> 此功能依赖于PHPUnit/Para/Pest的功能 - 它使用适当的命令行参数运行测试，并在VSCode中方便地显示覆盖率信息。请确保您的`phpunit.xml`配置包含`<source>`元素。对故障进行排查，请查看_OUTPUT_窗口/_PHP (Test Explorer)_。

### 更多功能

- 鼠标工具提示中的`@see`包含可点击的链接到引用的符号（如果可能）。
- 源代码中的`@see`具有语义着色的符号。
- **PHP 8.5**语言级别，管道操作符（`|>`）和基础检查。
- `enum`声明的验证（[#926](https://github.com/DEVSENSE/phptools-docs/issues/926)）。
- 检查隐式可空参数（在PHP &gt;= 8.4中已弃用）。
- 当运行包含多个测试套件的所有测试时，现在只会创建一个进程。

## 1.61.17926 (2025年9月23日)





### 改进

- `"search.exclude"`的行为在_查找所有引用_、_代码镜头_、_查找实现_、_工作区中的符号_中统一。
- 针对PHP &lt;8.4中没有括号的`new`成员调用进行诊断。
- Pest函数尊重新的`$this`。与任何使用`@param closure($this)`或`@param-closure-this`注释的参数有关（[#918](https://github.com/DEVSENSE/phptools-docs/issues/918)）。
- 针对不可达的匹配臂的诊断（[#919](https://github.com/DEVSENSE/phptools-docs/issues/919)）。
- 更改了函数参数代码片段补全的工作方式，这符合语言服务器协议并避免了VSCode的不必要警告（[#909](https://github.com/DEVSENSE/phptools-docs/issues/909)）。

### PHPUnit、Pest和数据集

我们正在为_测试资源管理器_引入新功能：支持更新的paratest、对Pest的实验支持以及在测试资源管理器UI中直接支持数据集。

![测试资源管理器中的数据集](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/testexplorer-datasets.png)

### 修复

- 修复了重载检查，并提供了实现缺失抽象方法的快速修复（[#2392](https://community.devsense.com/d/2392)）。
- 修复了在数组初始化中，在新行后的`[`后出现多余空格的问题（[#923](https://github.com/DEVSENSE/phptools-docs/issues/923)）。
- 当启用了`php.format.rules.spaceWithinDeclParens`时，为lambda表达式添加空格（[#922](https://github.com/DEVSENSE/phptools-docs/issues/922)）。
- 修复了PHP手册中类符号的_转到定义_功能。

## 1.60.17873 (2025年9月2日)




### 修复

- 参数完成代码片段（设置 `php.completion.parameters` == `"parameters"`）包含默认参数值，如预期一样。
- 修复内联CSS和脚本标签中的自动完成 [#914](https://github.com/DEVSENSE/phptools-docs/issues/914)

## 1.60.17845 (2025年8月23日)





### 改进

- 检查无效的PHP配置或可能导致调试中断的配置；所有警告都列在`OUTPUT` / `PHP`日志中。
- 改进了在`trait`内的类型推断，因此在`static::`、`self::`、`parent::`之后的成员大多数都能得到解析。编辑器会跟踪给定`trait`的所有使用情况，并查看`@extends`和`@mixin`注释。

### 调试

修复了某些断点被错误标记为未验证的问题。

### 修复

- 带有`@closure-this`或`@param callable(TYPE $this)`的lambda函数中的`$this`在工具提示中被标注为正确的类型。
- “重写抽象”代码操作生成正确的类型命名空间。
- 正确解析`@method static static`标签。
- 删除工具提示中围绕复杂类型名称的不必要的括号。
- 正确解析`trait`中的`self`和`static`。

## 1.60.17803 (Aug 14, 2025)





### 简化 `&&` 代码操作

现在可以将带有调用链 `->` 和与操作符 `&&` 的长条件简化为带有 `?->` 的单一调用链。

### 改进

基于用户反馈，进行了各种类型推断改进。

新的，通过魔术方法 `__call()` 调用的方法被标注为 `PHP6615` 诊断。这会在工具提示和编辑器中显示。新的诊断有助于避免不正确的方法调用。

![不正确的方法调用](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/err-call-via-magic.png)

### 修复

- 修复了当前文件中符号的导航。
- 修复了导航到 PHAR 文件中的符号。
- 修复了使用简单 `"/"` 通配符模式的 `"php.problems.exclude"` 设置。
- 修复了导致 `/vendor/` 中函数类型错误的 `array` 类型信息。
- 修复了在属性 hooks 中使用的类被错误检测为未使用的导入。
- 修复了 `method_exists()` 的含糊 `$class_or_object` 参数分析。
- 改进了在类型推断不明确情况下的方法检查。

## 1.59.17706 (2025年7月29日)





### 次要功能

- 将魔术方法移动到自动完成列表的末尾 [#690](https://github.com/DEVSENSE/phptools-docs/issues/690)。
- 改进了从模型“casts”推断的Eloquent模型属性的类型信息。
- 提供修复错误魔术方法修饰符的代码操作。
- 改进了复杂泛型中`static`类型的解析。

### 修复

- 修复了标准常量的错误弃用警告 [#2328](https://community.devsense.com/d/2328)。

## 1.59.17685 (2025年7月23日)





### 修复

- 修复了在存在 `__get()` 魔术方法时，关于未定义属性的错误警告的回归。

## 1.59.17674 (2025年7月18日)





### Laravel IDE 改进

- 在代码补全和导航中支持 Livewire 计算属性。
- IntelliSense 显示来自各种 Laravel 包（例如 Filament）的补全（视图、翻译键、路由、配置键）。
- Laravel 关系方法可以使用泛型，返回类型为 `HasOne<T,G>`，关系属性将具有 `T` 类型。
- 在找到相应的组件类时，在 Blade 文件中用正确的类型补全 `$this`。
- 补全 `casts()` 方法或 `$casts` 属性中找到的 Eloquent 属性。
- 修复了 Blade 文件中的 `@error` 指令。

### 格式化

- 添加了关于一元否定符之前空格的设置 [#874](https://github.com/DEVSENSE/phptools-docs/issues/874)。
- 修复了在单行属性钩子中，闭合大括号被放置在新行的问题 [#878](https://github.com/DEVSENSE/phptools-docs/issues/878)。

### 诊断改进

代码诊断总体上得到了改进，以避免虚假的警告。这修复了之前检查过的未知类名的报告、虚假的未实现抽象方法、某些数值运算中的无效类型推断等问题。

此外，编辑器现在检查未实现的抽象属性（[#870](https://github.com/DEVSENSE/phptools-docs/issues/870)）。

修复了 [#2322](https://community.devsense.com/d/2322)、[#2272](https://community.devsense.com/d/2272)、[#2286](https://community.devsense.com/d/2286) （及相关问题）。

### 次要改进

- 在没有 traits 的情况下进行返回类型提示中的代码补全 ([#887](https://github.com/DEVSENSE/phptools-docs/issues/887))。
- 修复了 "todo" 标记的 "跳动" 黄色高亮 ([#893](https://github.com/DEVSENSE/phptools-docs/issues/893))。
- 修复了来自 traits 的成员的覆写检查 ([#890](https://github.com/DEVSENSE/phptools-docs/issues/890))。

## 1.59.17515 (2025年6月23日)





### 排序 'use' 语句

现在可以将 'use' 语句的顺序设置为 `alphabetic` 或 `by_length`。这可以在 `settings.json` 或 `.editorconfig` 中设置，其中对应的 `ij_php_import_sorting` 指令会被尊重。

要排序 `use` 语句，请参阅[文档页面](https://docs.devsense.com/vscode/code%20actions/organize-uses/)。你可以使用代码操作进行排序、在文件保存时自动排序或作为自动修复进行排序。

### Laravel IDE 改进

- `.php.` 语言文件被处理——像 `trans()`, `__()`, 或 blade 的 `@lang` 方法将提供具有可能翻译键的补全和导航。
- IntelliSense 中更多的模型属性被键入。

### 修复

- 修复了在 blade 文件中补全代码片段时插入两个 `@` 的问题 ([#867](https://github.com/DEVSENSE/phptools-docs/issues/867))。
- 修复了在命名空间名称中解析 `Return` 的问题。
- 修复了某些 polyfill composer 包导致语言服务器崩溃的问题 ([#873](https://github.com/DEVSENSE/phptools-docs/issues/873))。

## 1.59.17478（2025年6月15日）




### 提取方法，提取常量

新的代码操作，可以将代码选择部分提取为函数或常量。

### Composer IntelliSense 增强

因为 `composer.phar` 通常位于工作区文件夹之外，因此编辑器无法识别其定义，我们已包含 `composer` IntelliSense 数据库（存根）。

无需进行任何操作，编辑器将识别 `/vendor/composer/` 文件中使用的 Composer 类，因此不会被报告为未知，并且可以进行检查。

如果用户正在开发例如 _Composer_ 插件，他们有两个选择：
- 将 `composer.phar` 添加到工作区以获得 IntelliSense（不过这样会消耗不必要的内存），
- 或者最好通过设置 `"php.stubs": ["composer", "*"]` 或使用命令 `> Workspace Stubs` 将 `composer` 存根添加到工作区中。

### IntelliSense 增强

- 通过 `new self`、`new static` 或 `new parent` 导航到构造函数（[#857](https://github.com/DEVSENSE/phptools-docs/issues/857)）。
- 导航优先考虑当前文件中的符号，如果有歧义的话。
- 处理以 `-string` 结尾的保留 PHPDoc 类型。
- 改进对 `.phpstorm.meta.php` 注释的未记录功能的处理。
- 检查复杂 Trait 方法的使用。
- 如果在全局代码和 Blade 模板中正确标注，则 `$this` 的使用不会被报告。
- 对作为 `callable` 参数的参数使用的可调用字符串的引用（[#2295](https://community.devsense.com/d/2295-to-go-definition-on-callable-params-in-function-call)）。
- 审查并修正所有内置 PHP 定义的 URL。

### Laravel 和 Eloquent

- 关系方法中的动态属性无缝添加到 IntelliSense 中。它们的类型从可选的泛型类型注释中推断。
  ```php
  /** @return HasOne<T> 使用泛型类型注释来指定动态属性 `$relationship` 的类型。 */
  function relationship(): HasOne { ... }
  ```
- 改进了 Laravel/Eloquent 魔术方法的隐式类型，例如 `Model::find(int)` 或 `Container::make()`。

### 格式化

- 防止 `foreach` 语句自动折叠为单行，以提高可读性。
- 修复了在 JavaScript 格式化程序中启用 `javascript.format.semicolons` 阻止 PHP 格式化程序应用更改的问题 [#850](https://github.com/DEVSENSE/phptools-docs/issues/850)。
- 修正文档注释块中包含制表符和空格组合时的格式。
- 修正交集类型的格式化问题 [#2309](https://community.devsense.com/d/2309)。

### 新设置

- `php.files.exclude`：Glob 模式用于从 PHP 语言服务器索引中排除文件和文件夹，但不从 VSCode 的资源管理器视图中排除。
- `php.navigation.referencesScope`：选择 "前往引用" 是严格的（需要严格类型化的对象类型），还是可以解析到任何可能的目标位置。
- `phpTools.parallelismLimit`：允许限制用于读取磁盘文件、解析和索引的后台线程数量（用户机器设置）。

### 不兼容更改

HTML 自动更新标签一直处于启用状态。现在它遵循 VSCode 设置 `"editor.linkedEditing"`，如 [code.visualstudio.com](https://code.visualstudio.com/docs/languages/html#_auto-update-tags) 上所述。

### 修复

- 性能改进。
- 修复 Trait 成员可见性更改的问题（[#854](https://github.com/DEVSENSE/phptools-docs/issues/854)）。
- 修复 Blade 解析器的问题。

## 1.58.17223 (2025年5月2日)





### 方法重写

已添加用于实现选定方法重写的代码操作。点击类头部，打开快速修复菜单（灯泡），并选择 `Override Methods`。在打开的快速选择面板中，勾选一些或所有可重写的方法，并确认。

![Implement Method Overrides](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vscode-method-overrides.gif)

### 次要功能

- 更新集成的PHP手册和IntelliSense，添加了（未记录的）PHP 8.4定义（[#841](https://github.com/DEVSENSE/phptools-docs/issues/841)，[#823](https://github.com/DEVSENSE/phptools-docs/issues/823)）。
- 遵循并建议 `@(psalm|phpstan)-require-(extends|implements)`；用于类层次验证、成员代码补全和代码导航（[#837](https://github.com/DEVSENSE/phptools-docs/issues/837)）。
- 遵循 `@param-closure-this`（[#825](https://github.com/DEVSENSE/phptools-docs/issues/825)）。
- 改进了从lambda或任何间接函数调用传递 `&` 引用的诊断（[#831](https://github.com/DEVSENSE/phptools-docs/issues/831)）。
- 大纲显示属性和类常量的可见性。
- 修复了混合JS/PHP代码的格式。[#2259](https://community.devsense.com/d/2259-a-comment-to-ignore-formatting-including-js-blocks)
- `Request::user()` 或 `Auth::user()` 的返回类型更加专业化，提供了更好的 `->` 后代码补全。

### 修复

- 修复了blade格式化器缩进过远的问题。
- 修复了在绑定到域的Unix系统上的崩溃问题。
- 修复了类体之后有注释时不必要的换行。
- 修复了PHP属性后的内联注释在格式化时被移到单独一行的问题 [#2245](https://community.devsense.com/d/2245-class-property-comment-after-goes-to-below-it-after-format)

## 1.57.17158 (April 11, 2025)





### 新特性

**`"search.exclude"`** 设置适用于_查找引用_和_工作区符号_功能（[thread #780](https://github.com/DEVSENSE/phptools-docs/issues/780)）。

### 小的改进

- 更新了集成的PHP手册和智能感知。
- 改进了`instanceof`类型的推断（[#810](https://github.com/DEVSENSE/phptools-docs/issues/810)）。
- 如果在`Closure::bind()`中，尊重匿名函数的`newScope` - 修复了错误警告并改进了代码补全。

### 修复

- 修复了作为命名参数传递的匿名函数的检查（[#821](https://github.com/DEVSENSE/phptools-docs/issues/821)）。
- `"files.exclude"`模式与VSCode中的处理方式相同。此前存在一些行为差异，现在应该解决了。
- `"files.exclude"`和`"search.exclude"`模式都是区分大小写的。

## 1.57.17031 (2025年3月25日)





### 新功能

全新推出的**代码操作**和文本选择的快速修复**进行了分组**。因此，可以一次对选择区域内的所有出现进行相同的操作。

![grouped code action](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-grouped-action.png)

选择一部分代码并对所有出现应用快速重构。这是另一个简化代码清理的增强功能，此外还有 [自动修复](https://docs.devsense.com/vscode/code%20actions/autofix/) 功能。

### 改进

- 对于 PHP >= 8 的 `explode()` 的分析正确推断为类型 `string[]`，不再包括 `bool` ([#2129](https://community.devsense.com/d/2129-wrong-variable-type-after-test))。
- 报告类型分析可能不完整，导致可能不完整的补全。这是由内部技术限制引起的，将在未来解决。
- 在生成的 `_ide_helper.php` 文件中有不明确/冗余定义时，更加支持 Laravel 的魔法功能。
- 报告函数内未使用的 `global` 变量。

### 修复

- 修复旧样式构造函数的问题。
- 修正含有保留 PHP 关键字的 FQN 的代码补全和诊断功能。
- 固定从 Model 的 PHPDoc 属性建议 Eloquent 列名。
- 可能的修复/改进：当存在不必要的 `@mixin` 导致类定义中循环时。
- 移除标识符名为“and”或“or”后的不必要空格 [#816](https://github.com/DEVSENSE/phptools-docs/issues/816)。
- 修复 Blade 文件中链接的 Ctrl/Cmd+点击功能 [#815](https://github.com/DEVSENSE/phptools-docs/issues/815)。
- 修复未保存（未命名）文档中的代码操作。

## 1.57.16971 (2025年3月12日)




### 次要功能

- 更新了PHP手册/IntelliSense，以支持新文档化的PHP 8.4声明。
- 在`app()`、`App::make()`等中支持Laravel服务ID自动完成。
- Eloquent的`find(int)`获得更具体的IntelliSense。
- 支持导航到`.phar`文件条目。
- 改进了一些边缘情况的诊断和自动完成。
- 遵循基声明中的`@param`（[#804](https://github.com/DEVSENSE/phptools-docs/issues/804)）。
- 现在支持在Docker/远程运行时利用`pathMappings`进行性能分析。性能分析数据将暂时存储在`/.vscode/profiling`工作区文件夹中（[#800](https://github.com/DEVSENSE/phptools-docs/issues/800)）。
- HEREDOC/NOWDOC字符串中的颜色（[#754](https://github.com/DEVSENSE/phptools-docs/issues/754)）。注意，有些主题不支持。
- 现在可以在PHP文件的HTML部分提供可点击的链接。

### 修复

- 修复了Blade大括号的自动完成问题。
- 修复了在特定场景下出现的Blade格式问题。

## 1.56.16884 (2025年2月19日)




### 次要功能

- 支持在 PHPDoc 结构化类型名称中的行注释。
- 支持 `template-type<,,>` PHPStan PHPDoc 类型函数。
- 更好的数组解包类型推断。
- 对于旧的 `Collection`，更好的 `foreach` 控制变量类型推断。
- 遵循 `if` 语句上方的 `@var` 注释。
- 更好的 `array_find()` 返回类型推断。

### 格式

- 修复了 `php.format.rules.blankLinesBeforeClass` 未正确应用于匿名类的问题。
- 在构造函数参数中添加对属性钩子的支持。[#786](https://github.com/DEVSENSE/phptools-docs/issues/786)
- 修复了在构造函数参数中提升的非对称属性的格式问题。[#788](https://github.com/DEVSENSE/phptools-docs/issues/788)
- 修复了当 `.editorconfig` 选项 `ij_php_blank_lines_around_method` 设置时，在 lambda 函数前出现不必要空行的问题。[#818](https://github.com/DEVSENSE/phptools-docs/issues/818)

## 1.56.16853（2025年2月12日）




### Laravel

- 为 Eloquent “魔术”方法和 Laravel 特定函数提供代码补全。
- 通过特殊的 `ide.json` 文件进行可扩展的代码补全。
- 在 `config(..)`、`config()->string(..)`、`Config::get(..)` 等中提供配置键的补全。
- 提供环境变量的补全。
- 在 Laravel 特殊函数中提供视图属性的补全。
- 在特定函数中提供命名路由的补全。
- 在特定函数中提供路由参数名称的补全。
- 在特定函数中提供语言翻译文件中的 ID 的补全。

### Eloquent

- 在各种 Eloquent 查询构建器方法中补全模型列。列从以下内容解析（优先级依次为）：
  - 模型类 PHPDoc 中的 `@property`。
  - 模型工厂类的 `definition()` 函数。
  - 使用模型表（如果能解析），查找 `database/migrations/` 中的迁移和 `Schema` 定义。
- 补全模型动态字段。
- 补全魔术 `whereCOLUMN()` 函数。

### Laravel Blade

- 补全使用 `Blade::component()` 定义的组件别名。
- 补全使用 `Blade::include()` 定义的视图别名。
- 从 `ide.json` 中补全组件。
- 从 `ide.json`、`Blade::directive()` 和 `Blade::if()` 中补全指令和条件指令。
- Livewire：在 `wire:model` 值中补全/导航组件属性。
- Livewire：在 `wire:***` 值中补全/导航组件动作。
- 补全部分名称。
- 将 `x-dynamic-component` 添加到补全中。
- Blade 格式化和折叠尊重自定义 `if` 指令。
- 自动在 `{{}}` 或 `{{{}}}` 内插入空格。
- 当键入 `{!` 时自动插入 `{!! !!}`。
- 当键入 `{{-` 时自动插入 `{{-- --}}`。
- 使用命令 `phptools.blade.switchViewClass` 在视图和类文件之间切换。转到“打开键盘快捷键”-> 搜索“phptools.blade.switchViewClass”-> 分配快捷键。

### HTML

- 现在 HTML 属性的自动插入引号后立即出现补全列表。

### 格式化

- 添加了 `php.format.rules.blankLinesBeforeReturnStatement` 以定义 return 语句前的空行数。
- 添加了 `php.format.rules.blankLinesAroundProperty` 以定义属性周围的空行数。
- 添加了 `php.format.rules.blankLinesAroundClassConstant` 以定义类常量周围的空行数。
- 添加了 `php.format.rules.blankLinesAroundEnumCase` 以定义枚举案例周围的空行数。
- 扩展了 PER 编码风格（`php.format.codestyle` 设置为 `per`），根据 [PHP PER 编码风格](https://www.php-fig.org/per/coding-style/) 强制执行空行限制。
- 解决了在使用 JavaScript 中多行模板字符串时 PHP 文件中不必要缩进的问题。[#2215](https://community.devsense.com/d/2215-unwanted-indentation/3)

### 调试

- 增强了调试器中对 `.env` 文件的支持。
- `envfile` 选项已弃用；请在 `launch.json` 中使用 `envFile` 进行环境变量配置。

### 修复

- 修复了编辑代码时三点和内嵌提示漂移的问题（[#776](https://github.com/DEVSENSE/phptools-docs/issues/776)）。
- 在 `.blade.php` 文件中嵌入 PHP 代码时，排序和移除使用项，以及 `editor.codeActionsOnSave` 的补全问题已修复（[#483#issuecomment-2621398221](https://github.com/DEVSENSE/phptools-docs/issues/483#issuecomment-2621398221)）。
- 工作区符号不列出 `vendor` 中的文件和 `"files.exclude"` 设置中指定的文件夹。
- `.phar` 文件在 composer 包中不会被忽略，且 `.phar` 文件中的定义会正确地包含在 IntelliSense 中。

## 1.55.16740 (2025年1月22日)




### 修复

- 修正了多行方法参数属性的缩进 [#767](https://github.com/DEVSENSE/phptools-docs/issues/767)
- 适当显示了返回类型提示 `Generator`，用于返回值的函数（生成器）。
- 修复了扩展每次启动时尝试重新激活试用许可证的错误。
- 修复了指定路由脚本时 Profiler 的使用。
- 修复了多次请求时 Profiler 的使用 - 所有探查器输出均被打开。详见 [Profiler 文档](https://docs.devsense.com/vscode/profiling/?h=profiler#quickly-setup-php-for-profiling)。

### 次要特性

- 代码流分析推断出生成器的完整 `Generator<TKey,TValue,TSend,TReturn>` 类型，从而改善了 `foreach` 迭代生成器时的类型推断、`Generator::send()` 的类型检查和 `Generator::getReturn()`。
- 在 `Route::` 类似函数中对 Laravel 路由参数进行着色。
- 新增探查启动配置（当没有 `launch.json` 且用户按下 _Start Debugging_ (`F5`) 时）。

## 1.55.16685 (2025年1月15日)





### 更多Laravel支持

- 对Laravel视图和命名空间视图的自动完成和导航。
- 对`route()`函数中Laravel路由名称的自动完成和导航。
- 对Blade文件中组件 (`<x-...`) 的自动完成和导航。
- 对`<livewire:`之后的Livewire组件的自动完成和导航。
- 对`@livewire()`和`Livewire::mount()`中的Livewire视图的自动完成和导航。
- 对来自视图类属性、Livewire `mount()`和`@props()`指令的组件属性的自动完成和导航。
- 对`@includeWhen`、`@includeUnless`和`@each` Blade指令中的视图的自动完成。
- 对特定Laravel函数 (`asset`, `storage`, ...) 路径的自动完成。
- 在`Blade`语言中启用了PHP功能（智能感知、内联提示、代码透镜、导航等）。

### 格式化

根据在[#2195](https://community.devsense.com/d/2195-add-new-blank-line-settings-and-update-psr-12-and-per-styles)上的请求，我们引入了一些新的格式设置：

- `php.format.rules.blankLinesBetweenUseTypes`：指定不同类型的`use`语句（例如类、函数、常量）之间的空行数。这不会影响同一类型语句之间的空行。
- `php.format.rules.blankLinesAfterOpenTag`：指定在开放标签后插入的空行数，除非闭合标签在同一行上。

查看[Customize Formatting](https://docs.devsense.com/vscode/editor/customize-formatting/#blanklines)了解更多细节。

### 修复：Laravel项目的默认启动配置

- 修复了默认启动配置，以正确使用Laravel路由器脚本。
- 如果没有`.vscode/launch.json`文件，只需打开一个`.php`文件并按`F5`。默认启动动作将启动并调试开发Web服务器（假设已安装Xdebug）。
- 此外，初始的`launch.json`配置现在包含了针对Laravel项目的正确启动设置。

> 此修复影响到快速内置开发服务器的使用，每当Web根目录位于子文件夹中时，例如在`/public`、`/wwwroot`或`/webroot`中有`index.php`。现在，内置开发服务器以与Web根目录相同的工作目录启动，例如`${workspaceFolder}/public`。如果没有`.vscode/launch.json`文件，可以尝试按`F5`开始调试。

### 小功能

- 在工具提示和内联类型提示中显示结构化对象类型。
- 改善类型推断，更好地利用`class-string<T>`注解。

### 修复

- 从抽象类运行测试[#753](https://github.com/DEVSENSE/phptools-docs/issues/753)。
- 文档注释中的浮点和整数字面量[#752](https://github.com/DEVSENSE/phptools-docs/issues/752)。
- 无效的多余括号提示[#750](https://github.com/DEVSENSE/phptools-docs/issues/750)。
- 括号内表达式的鼠标悬停和自动完成[#743](https://github.com/DEVSENSE/phptools-docs/issues/743)。
- 条件表达式后的自动完成。
- 在`laravel\framework` >= `11.30`中自动解析默认别名。
- 从基类解析方法的返回类型。
- 解决了在某些格式化规则配置下，每次格式化时Blade文件中`@php`指令内部第一行进一步向右缩进的问题([#548](https://github.com/DEVSENSE/phptools-docs/issues/548))。
- 修复了在Blade文件格式化期间控制流指令后出现不必要空格的问题。

## 1.54.16574 (2024年12月23日)





### 代码操作

- 添加了类成员修饰符顺序的代码操作（根据 PSR-12）以及缺少可见性修饰符的代码操作。

### 改进

- 在工具提示和提示中简化了结构化数组（[#703](https://github.com/DEVSENSE/phptools-docs/issues/703)）。
- 更好的代码补全和 `->` 操作符、赋值表达式后的鼠标悬停效果，以及无括号的 `new` 之后。

### 修复

- 新的 `...(set)` 关键字后的补全/悬停/转到定义。
- 通过 `static::` 引用的类成员的引用计数。
- 构造函数属性中的新 `...(set)` 修饰符。
- 在其他文件中重命名全局变量时显示预览。
- 不再以区分大小写的方式检查 PSR 自动加载的类名（与 VSCode API 和 FileSystem API 存在问题 [#635](https://github.com/DEVSENSE/phptools-docs/issues/635)）。
- 修复了在 lambda 函数中函数名后不需要的空格 [#2196](https://community.devsense.com/d/2196-no-spaces-after-function-name-formatting-rule)。
- 在具有不对称可见性的属性中导航 [#741](https://github.com/DEVSENSE/phptools-docs/issues/741)。

### 重大变更

- 扩展不再捆绑旧的 PHPUnit 6 二进制文件。当运行 PHPUnit 测试时，用户需要安装 "phpunit/phpunit" composer 包或指定 `"phpunit.phpunit"` 设置值。

## 1.54.16480 (2024年12月10日)





### PHP 8.4 语法

编辑器支持新的 PHP 8.4 非对称可见性语法（[#728](https://github.com/DEVSENSE/phptools-docs/issues/728)）。如果您的 PHP 版本尚不支持，语法将显示为错误下划线。

### 配置文件测试与启动配置文件

测试资源管理器可以运行、调试和新增的性能分析 PHPUnit 测试（如果安装了 [PHP Profiler](https://marketplace.visualstudio.com/items?itemName=DEVSENSE.profiler-php-vscode) 扩展）。详见 [Profiling Tests](https://docs.devsense.com/vscode/test-explorer#profiling-tests)。

此外，可以使用 [自定义 `launch.json`](https://docs.devsense.com/vscode/test-explorer#custom-debug-launch-profile) "php" 配置文件来运行测试。 

### 代码操作有标识

更多代码操作已被记录（请参阅 [Code Actions List](https://docs.devsense.com/en/vscode/code%20actions/list)），因此可以 [隐藏](https://docs.devsense.com/vscode/code%20actions/hide-code-action) 或标记为自动修复。[自动修复](https://docs.devsense.com/vscode/code%20actions/autofix) 是一个方便的功能，允许您在文件保存时或者使用"自动修复"命令时自动应用有用的代码操作（如果有）。

### 改进

- 在语法上破损的文件中更好地建议变量名。
- 为通过引用赋值非变量提供了更具体的警告信息。
- 增加了 PHP 手册的 **意大利** 语言版本。使用命令 `> PHP Manual Language` 或设置 `"phpTools.language": "it"`。请注意，未翻译的文本将以英语显示。
- 运行 PHPUnit 测试速度更快（[#725](https://github.com/DEVSENSE/phptools-docs/issues/725)）。在可能的情况下，特定文件路径会传递给 PHPUnit，以避免扫描所有内容。
- 可以在工作区范围设置中更改 `"php.executablePath"` 设置。
- `"php.executablePath"` 和 `"php.executables"` 可以包含变量，例如 `"${workspaceFolder}/bin/php"`。
- **ORM**：在类 `T` 上使用相应的 `#[ORM\Entity(repositoryClass)]` 属性时，推断调用 `EntityManager::getRepository(class-string<T>)` 的存储库类 ((#2174)[https://community.devsense.com/d/2174])。
- 添加了 WordPress 和 PER 代码风格所需的代码修复。

### 修复

- 解决了 `php.format.rules.maxBlankLines` 设置在文件末尾未正确应用的问题。[#2188](https://community.devsense.com/d/2188-maxblanklines-does-not-work-properly-at-the-end-of-a-file)
- 更新了 Laravel 代码风格，将匿名类型的开括号置于新行上，以确保与 Laravel 约定对齐。[#734](https://github.com/DEVSENSE/phptools-docs/issues/734)
- Laravel 代码风格在函数声明中移除返回类型前的空格 [#734](https://github.com/DEVSENSE/phptools-docs/issues/734)
- 修复了在 `/vendor/` 文件夹中声明的派生类中使用模板类型参数的问题（例如 ORM 的 `EntityManager::getReference()`）。

## 1.53.16379 (2024年11月19日)





### 代码操作设置

现在可以更改**代码操作严重性**。这意味着某些重构或建议的快速修复可以被隐藏或标记为警告或错误。

要隐藏代码操作，可以使用以下方法之一：

- 对应的快速修复“不要显示”
- 或者将代码操作添加到 VSCode 设置中的 `"php.problems.exclude"`。
- 或者将代码操作添加到您的 `.editorconfig` 文件中。

要改变其严重性，请将代码操作添加到您的 `.editorconfig` 文件中。以下示例将所有冗余的闭合标签 `?>` 标记为错误，迫使您清理它们：

详情如下：

- [设置代码操作严重性](https://docs.devsense.com/en/vscode/code%20actions/severity)
- [隐藏代码操作](https://docs.devsense.com/en/vscode/code%20actions/hide-code-action)

```ini
[*.php]
php_remove_redundant_closing_tag = error
```

**代码操作自动修复**：现在代码操作可以作为自动修复运行。详见 [自动修复](https://docs.devsense.com/en/vscode/code%20actions/autofix)。

### 诊断

- 新的诊断检查在右侧使用 trait 的 `instanceof` 无效用法。

### 修复

- 索引 `vendor` 文件夹中的元文件。
- 索引指向 VSCode 工作区外部的 `vendor` 中的符号链接包 ([#684](https://github.com/DEVSENSE/phptools-docs/issues/684))。
- 修复了删除光标后文本的问题 ([#638](https://github.com/DEVSENSE/phptools-docs/issues/638))。

## 1.53.16338 (2024年11月12日)





### 格式化

我们很高兴地宣布在扩展中引入了一个新的 **PER** 代码样式选项，与 [PHP-FIG PER 编码样式标准](https://www.php-fig.org/per/coding-style/) 保持一致。此编码样式旨在帮助 PHP 开发人员维护遵循最新行业标准的一致、高质量代码。通过使用 **PER**，您可以确保项目的代码遵循标准化格式，增强代码的可读性、可维护性以及与其他开发人员的协作。

![PER代码样式](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/settings-codestyle-per.png)

要应用此样式，只需在您的配置设置中将 `"php.format.codestyle"` 设置为 `"per"`，格式调整将自动应用于您的项目。这个新选项是简化代码格式化并确保您的 PHP 代码库与 **PER** 指南保持一致的绝佳方式。祝您编码愉快！

### 代码操作

[Sort Uses Code Action](https://blog.devsense.com/2023/sort-uses-and-remove-unused-uses-on-php-file-save) 是一个强大的工具，可以在多个上下文中使用：作为代码操作、在自动导入期间，以及与 `editor.codeActionsOnSave` 设置结合使用。此功能允许开发人员自动按一致顺序组织 `use` 语句，使代码更简洁易读。

要进一步自定义此功能的行为，您可以控制其大小写敏感性。设置 **`"php.sortUses.caseSensitive"`** 让您指定排序是否应考虑大小写敏感性。将此选项设置为 `true` 以进行区分大小写的排序，或者设置为 `false` 以进行不区分大小写的排序。默认情况下，排序**不区分大小写**，因此所有 `use` 语句在排序时不区分大小写。

更多详情，请查看我们社区论坛上的相关讨论 [#2127](https://community.devsense.com/d/2127)。

### 诊断

- 添加了使用无效类名（即保留类名）的诊断。

### 修复

- Copilot 聊天窗口不会中断 IntelliSense 和代码诊断；关闭后由 Copilot 聊天建议的更改将被忽略。
- 修复了在类和该类使用的特性之间查找引用的问题。
- 修复了索引链接在项目文件夹外的Composer包的问题。
- 修复了当类名为“parent”或任何其他保留关键字时语言服务器崩溃的问题。

## 1.52.16273 (2024年10月30日)




### `.editorconfig`中的格式设置

现在，可以使用标准的`.editorconfig`文件完全调整代码格式规则。详情请参阅["customize formatting"](https://docs.devsense.com/vscode/editor/customize-formatting)。

### 改进

- 工具提示文本将PHPDoc摘要格式保持原样 (#2145)[https://community.devsense.com/d/2145]。
- 类型推断改进。
- 添加快速操作以全局忽略特定诊断。

### 修复

- 修复`function`导入代码操作。
- 修复键入时的格式。
- 诊断: `FFI\CData`可以用作数组。

## 1.52.16226（2024年10月21日）




### 功能

- 新增 **`PHP > Format Multiple Files`** 命令，允许您批量格式化多个 `.php` 文件。首先输入 **glob 模式**。所有格式更改将首先收集并显示在 **预览窗口** 中。文件将在确认后进行修改。
- 新增 **代码操作**，用于将完全限定函数名称更改为别名（[#693](https://github.com/DEVSENSE/phptools-docs/issues/693)）。
- 新增设置 **`php.format.exclude`**。这允许指定一个或多个 glob 模式，用于不使用 PHP 格式器格式化的文件。这包括 `formatOnType`、文档格式化、`formatOnSave` 和选择格式化。在使用新的 `Format Multiple Files` 命令时，排除的文件将在最终格式评审中自动取消选中。

### 改进

- 默认语言级别更改为 8.3。
- 插入带命名参数的内嵌提示仅在语言级别设置为 PHP 8.0 或更高时通过双击实现（[#686](https://github.com/DEVSENSE/phptools-docs/issues/686)）。
- 默认情况下 `.vscode-server` 被排除在索引之外（[#2132](https://community.devsense.com/d/2132)）。
- 同时兼容 `@property-write` 和 `@property-read`。
- 工具提示中的结构化数组语法（数组类型在工具提示中不再被过度简化）。
- `callable()` 与 `...` 能够正确解析，并在工具提示中显示可变参数，同时在内联提示中得以尊重。
- `@template-contravariant` PHPDoc 关键字（[#695](https://github.com/DEVSENSE/phptools-docs/issues/695)）。
- 在使用 `use function` 构造或作为特征别名后补全函数名称时，不再插入括号。
- 解析 PHPDoc 泛型类型规范中的 `covariant` 和 `contravariant` 修饰符（[#699](https://github.com/DEVSENSE/phptools-docs/issues/699)）。
- 继承自类的 `@param` 注解得到尊重（[#702](https://github.com/DEVSENSE/phptools-docs/issues/702)）。
- 匿名函数的 `$this` 从包含的 `Closure::bind()` 调用中推断（[#701](https://github.com/DEVSENSE/phptools-docs/issues/701)）。

### 修正

- 修正了在 `@phpstan-import-from` 中使用时误报的未使用 use。
- 赋值上方的 `/** @var */` 注解不会影响后续类型匹配。
- 在非私有上下文中，`private` 类型的属性不再显示在代码补全中。
- Composer 的 `InstalledVersion.php` 被 IntelliSense 索引。
- 修正了诊断信息中的拼写错误。
- 修正了在使用魔术方法 `__get` 时关于私有属性的错误警告。
- 在 `identifier( new )->` 后的代码补全（[#678](https://github.com/DEVSENSE/phptools-docs/issues/678)）。
- 修正在 `default` 函数名后补全的问题（[#692](https://github.com/DEVSENSE/phptools-docs/issues/692)）。
- 修正了在 PHP < 8.1 中对 `ArrayAccess` 方法重写的错误检查（[#689](https://github.com/DEVSENSE/phptools-docs/issues/689)）。
- 修正在函数返回类型提示和关键字后的补全问题（[#670](https://github.com/DEVSENSE/phptools-docs/issues/670)）。

## 1.51.16099（2024年9月26日）




### 改进

- 检查按引用传递参数的特殊数组函数。
- 在 `composer.json` 中识别 `"php-64bit"` 的版本要求。 [#665](https://github.com/DEVSENSE/phptools-docs/issues/665)
- PHPDoc 中的 `Closure()` 仅带有 `...`。 [#661](https://github.com/DEVSENSE/phptools-docs/issues/661)

### 调试

- 添加了对 `skipEntryPaths` 设置的支持，该设置允许指定 glob 模式以在初始入口文件匹配时跳过。

### 修复

- 修复了通过 `::` 操作符导航到静态对象成员的问题（工具提示、转到定义、代码完成）。**[#666](https://github.com/DEVSENSE/phptools-docs/issues/666)** [#2126](https://community.devsense.com/d/2126)
- 修复了当工作区中排除了 `vendor` 时的索引问题 [#2100](https://community.devsense.com/d/2100)。
- 修复了 `FILTER_NULL_ON_FAILURE` 常量被误转为小写的问题 [#2085](https://community.devsense.com/d/2085-incorrect-auto-lowercasing-of-filter-null-on-failure-constant-in-php-code/8)。
- 默认情况下，在存根中包含 `sodium`。
- `object` 类型提示遵循结构化的 `object` phpdoc 类型提示。
- 在多个 `::` 表达式链之后，代码完成功能正常工作。
- 修复了模板类型参数在推断类型中绑定的问题 [#2106](https://community.devsense.com/d/2106-function-parameter-return-type)。
- 修复了在 composer 仍在运行时 composer 包的缓存问题。
- 修复了 `php.format.rules.alignConstants` 格式化问题，该问题导致在声明命名空间时无法正确对齐类上下文外的常量。[#2114](https://community.devsense.com/d/2114-alignconstants-not-always-working)
- 当 `vendor` 文件夹中有很多 composer 包时，初始索引速度更快。
- "auto-import" 将 `use` 添加到正确的命名空间范围。
- 修复了在有太多带有 `from` 别名的 `@import` 指令时可能导致语言服务器崩溃的问题。

## 1.51.15986 (2024年9月10日)




### 改进

- 不显示无用的工具提示 ([#611](https://github.com/DEVSENSE/phptools-docs/issues/611))。
- 通过间接类型访问静态类成员时尊重 `class-string<T>` 注解。
- 属性访问可见性检查。
- 在 PHP 文档块中统一颜色地着色常量值。
- 类型推断改进，必要时从基类继承 `@global` 标签。
- 重构建议 `switch`->`match` 仅用于 PHP>=8 ([#2098](https://community.devsense.com/d/2098))。
- 重构并查找引用以动态成员访问获取更好的结果 ([#2093](https://community.devsense.com/d/2093))。
- 默认启用标准的**插入提示**。

### 修复

- 修复从文件开头开始的代码折叠丢失。
- 修复双引号字符串中的变量补全。
- 修复对 `php.stubs` 的更新未被尊重。
- 修复在工作区内 `.phar` 文件的更新未包含在 IntelliSense 中的问题。
- 修复当赋值的左值是多行表达式时对齐 `php.format.rules.alignConsecutiveAssignments`。[#642](https://github.com/DEVSENSE/phptools-docs/issues/642)
- 修复类型化常量声明的鼠标悬停。
- 修复在接口上使用 `@extends` 的错误警告。
- 修复（重新启用）未知类警告的快速修复。
- 在包缓存中保留 `@internal` 函数（即保留在 IntelliSense 中）。

## 1.50.15906（2024年8月20日）





### 改进

- 类常量和枚举案例检查现在是区分大小写的。
- 泛型类型参数语法接受 `*` 令牌。
- PSR-4 同样检查 `"autoload-dev"` 规则。
- 更新了集成的 PHP 手册，增加了 `SimpleXmlElement::saveXml`。
- 更多传引用参数的检查。

### 修复

- 修复了在 Windows 上重命名文档后出现的问题，重命名文件时代码操作在字母大小写不同的情况下被破坏。
- 修复了 PSR-4 类名和文件路径检查及相应的重命名代码操作。
- 修复了 `is_numeric()` 后类型推断无效的问题。
- 修复了 `A ? A : B` 的错误重构建议。正确的应该是 `?:`。
- 修复了带有隐式可为 null、`never` 和 traits 的覆盖检查。
- 修复了在命名空间名称中使用 `Function` 关键字的问题。
- 修复了使用单个泛型类型参数的 `Collection<T>`。

## 1.50.15872 (2024年8月13日)





### 编辑器

- 突出显示结构化数组/对象类型中的名称 ([#597](https://github.com/DEVSENSE/phptools-docs/issues/597))。
- 使用 `keyword` 颜色突出显示 PHPDoc 标签名称和保留类型名称（取决于所选主题） ([#612](https://github.com/DEVSENSE/phptools-docs/issues/612))。
- 突出显示 trait `use` 上方的 PHPDoc 块。

### PHP 8.4 支持（预览）

此更新增加了对新 PHP 8.4 功能的支持，包括：

- 属性挂钩和 `__PROPERTY__` 魔术常量。
- 无括号的 `new`。
- 属性和属性挂钩的格式化。

### 格式化器空行设置

PHP 代码格式化器有一个全新的设置组“`Blank Lines`”，用于调整各种代码部分之间的空行。您可以调整声明、类体、注释、函数等上方的空格。查看设置以获取 `php.format.rules.blankLines***` 选项的完整列表。

### 功能

- `"php.docblock.colorMode"` 用户范围设置允许简化 PHPDoc 块的着色 ([#612](https://github.com/DEVSENSE/phptools-docs/issues/612))。
- 检查 PSR-4 自动加载规则、类名和文件名。 快速修复 PSR-4 文件名不匹配 ([#609](https://github.com/DEVSENSE/phptools-docs/issues/609))。

### 改进

- 调整了未导入全局类型的补全排序 ([#598](https://github.com/DEVSENSE/phptools-docs/issues/598))。
- 检查魔术常量（`__METHOD__`、`__PROPERTY__` 等）是否在正确的上下文中使用。
- 诊断改进，修正了 `try`/`finally` 控制流和可达性分析。
- 改进类型推断。

### 修复

- 修复了 HTML 折叠与 PHP 代码折叠交叉时的代码折叠问题。 ([#594](https://github.com/DEVSENSE/phptools-docs/issues/594))
- 修复了 `self` 的参数类型检查。
- 修复了函数或类上方使用 `@suppress` 的问题。
- 修复了格式化 `require` 和类似语句后出现多余空格的问题。
- 修复了当使用 `php.format.rules.arrayInitializersAlignKeyValuePairs` 设置格式化数组初始化器中的复杂表达式时的问题。
- 修复了在格式化期间代码块中出现不必要换行的问题。 [#2057](https://community.devsense.com/d/2057-formatting-sometimes-takes-2-passes/)

## 1.49.15728 (2024年7月8日)




### 改进

- 在声明上方输入 `/**` 后生成文档注释。此功能不再需要启用 `formatOnType`。
- 在双引号字符串中输入 `$` 后触发建议。
- 在文档注释中输入类型提示时触发建议。
- 初步支持 `@phpstan-assert`，`@phpstan-assert-if-true`，`@phpstan-assert-if-false`。
- PhpUnit 测试可在嵌套目录中被发现，并遵循 `prefix` 配置。
- 保存时的 `"source.organizeImports"` 代码操作不会移除未使用的 uses，因为这可能是不合意的。 ([#1883](https://community.devsense.com/d/1883))
- 为 `"editor.codeActionsOnSave"` 设置添加了显式代码操作：
    - `"source.source.sortImports"`：仅排序 uses。同 `"source.organizeImports"`。
    - `"source.source.sortAndRemoveImports"`：移除未使用的 uses 并排序其余。
- 识别未封闭数组形状类型 ([#587](https://github.com/DEVSENSE/phptools-docs/issues/587))
- Blade 支持短标签。

### IntelliSense

- Laravel 的 `Macroable::macro()` 在嵌套 lambda 函数内更好地推断 `$this`。
- `@param` 补全缺少的参数名称。

### 提示 (`...`)

带有可用快速重构的代码会用三个小点进行标注。鼠标提示提供更多细节和执行对应代码操作的快速修复。

![Quick Fix Hints](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-hint-quickfix.gif)

### 调试器

- 增加对 Unicode 数组键和属性名称的支持。
- 调试控制台为变量名提供补全。

### 修复

- 修复 `Align Properties` 格式规则，确保即使在连续格式化操作之后也能正确对齐。
- 修复在存在带模板参数的 `@extends parent<>` 注释时的崩溃问题 ([#585](https://github.com/DEVSENSE/phptools-docs/issues/585))。

## 1.48.15635 (2024年6月16日)




### 改进

- 改进初始索引，将测试用例的发现推迟到索引完成后。
- 优化，改善内存使用。
- 更好的 `ReflectionClass::getMethods()` 类型推断。
- 将日志记录统一到 OUTPUT 面板。
- 实现抽象函数时添加通用的 `@inheritDoc` 文档注释。
- `Sort uses` 代码操作会去除重复项。

### 格式化改进

#### 对齐属性

格式化器现在提供 `对齐属性` 功能，以对齐类定义中的属性，从而改善代码展示和可读性。可以使用 `php.format.rules.alignProperties` 选项激活此功能。

```php
class X
{
    var       $a   = 1;
    public    $bb  = 2;
    protected $ccc = 3;
}
```

### 修复

- 函数重写检查尊重 `#[ReturnTypeWillChange]` 属性。
- 修复关于作为数组使用的对象的虚假未使用变量警告 ([#533](https://github.com/DEVSENSE/phptools-docs/issues/533))。
- 修复当存在 `array()` 或单行块时的代码折叠问题。
- 修复在注释后立即进行代码补全的问题。
- 修复重命名和突出显示私有字段的出现。
- 稳定性修复。
- 修复在 php 与 javascript 混合时的格式化问题 [#2012](https://community.devsense.com/d/2012-php-file-with-mixed-php-and-javascript-using-in-vscode)

## 1.47.15512 (2024年5月28日)





### Blade `.blade.php` 支持

- 支持 `@use` 指令，包括类型别名。代码补全和 IntelliSense 正确识别导入和别名类。
- 高亮显示 HTML 标签内的 `@class` 指令和其他内容。
- 开始和结束的 blade 标签以 PHP 关键词和 HTML 开始/结束标记进行高亮显示。
- 提升在 blade 文件中的 PHP 代码补全、PHP 函数签名帮助和 PHP 代码折叠。
- 稳定性修复。

![Blade @Use completion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-blade-use.gif)

### 诊断

- 现在遵循 `/** @ignore $variablename */`，如果 `$variablename` 未被使用，将不会报告问题。
- 支持更复杂的条件返回类型，例如 `@return ($name is class-string<T> ? T : bool)` ([#538](https://github.com/DEVSENSE/phptools-docs/issues/538))。
- 修复了错误的不可达代码警告 ([#556](https://github.com/DEVSENSE/phptools-docs/issues/556))。
- 检查处理 `method_exists` 和 `function_exists` 以避免关于未知函数的错误警告。

### 新功能

- 从目标 `callable()` PHPDoc 类型注释推断 lambda 函数参数类型。
- 为推断出的 lambda 参数类型添加嵌入提示。启用 `"php.inlayHints.types.lambdaParameter"` 设置。

![Inlay for infered lambda parameters](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/inlay-lambda-parameter-type.png)

### 重命名重构

重命名重构已部分重新实现，新的重命名场景已被实现，并修复了各种情况。重构正确处理了类/常量/函数的导入、模板类型名、字符串和数组中的名称实例等。

#### 新功能

- **正确重命名别名类型名**，因此在重命名与原始类型不同的类型别名时，仅重命名别名。
- **正确重命名别名函数和常量**。
- **重命名泛型类型**已被修复和优化。
- **已实现重命名导入的模板类型**。这适用于各种 PHPDoc 标签，如 `@phpstan-import-from`、`@psalm-type` 等。
- **查找模板类型名和类型名的引用**已修复，并正确处理了新的场景。

请告知我们重命名重构是否存在问题——我们正努力改进。

_已知缺失功能：_ 重命名命名空间，重命名命名参数。正在进行中。

### 改进

- 对冒号块（`if:`、`switch:`、`while:`、`for:`、`foreach:`）的折叠支持。
- 改进了 `by-ref` 函数的鼠标悬停提示。
- Blade 格式化器在 `.blade.php` 文件中正确缩进 PHPDoc 块。
- 添加了函数头参数中的选择范围。
- 扩展选择范围到相应的 PHPDoc 块。
- 生成getter/setter时调整整个标识符以匹配 `"php.completion.namingConvention"` 设置。 ([#2011](https://community.devsense.com/d/2011-getters-setters-function-case))

### 修复

- 修复了命名参数之前发生的非预期空格，这些参数也是关键词。 [#555](https://github.com/DEVSENSE/phptools-docs/issues/555)
- 在停止调试会话后，所有 PHP 子进程都会被终止。 [#542](https://github.com/DEVSENSE/phptools-docs/issues/542)
- 修复了 _大纲_ 中有匿名 `class` 的问题 ([#557](https://github.com/DEVSENSE/phptools-docs/issues/557))。
- 修复了鼠标悬停时的 L-Value 变量类型。
- 修复了 lambda 函数中 `empty` 之后不需要的空格 [#564](https://github.com/DEVSENSE/phptools-docs/issues/564)
- 解决了在活动调试会话期间设置或删除断点导致 VSCode 错误标记为未验证的问题。

## 1.46.15409 (2024年5月9日)





### 功能

- `namespace` 后的内联建议。
- 折叠 Blade 块。
- Blade 标签补全。
- `.blade.php` 文件格式化（必须以 PHP 文件打开）。

### Blade 格式化

已经实现了 Blade（`.blade.php` 文件）代码的格式化。该格式化程序结合了 HTML/CSS/JS 和 PHP 的格式化输出以及 PHP 缩进，同时还包括 Blade 块的缩进。

目前还没有其他设置。基于您的反馈，我们将添加更多设置和修复！

![Blade Formatting](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-blade-format.gif)

> 请注意，如果您有其他的 Blade 扩展，此功能可能无法使用。请确保打开的 `.blade.php` 文件的语言设置为 `PHP`（位于 VSCode 窗口的右下角）。

### HTML 自动闭合标签和属性

在 PHP 代码中，当您输入打开标签的 `>` 时，HTML 标签元素现在会自动闭合。同样，当您输入闭合标签的 `/` 时，会无缝插入匹配的闭合标签。

此外，当您输入 `=` 时，HTML 属性引号现在会自动包含。

### 自动重命名 HTML 标签

HTML 标签的自动重命名现在默认启用。您可以使用以下设置在 VSCode 的 `settings.json` 中禁用此功能：

```json
"[php]": {
    "editor.linkedEditing": false
}
```

![Auto-Renaming HTML Tags](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-html-linkededit.gif)

### 改进

- 性能和内存使用的改进。
- 在 PHP 文件和 Blade 文件的 HTML 部分中缩小/扩大选择（`Shift+Alt+Left` 和 `Shift+Alt+Right`）。

### 修复

- 修复了 `static` 返回类型的覆盖检查问题。
- 修复了在修改 `.blade.php` 文件代码时的内嵌提示。

## 1.45.15272 (2024年4月11日)





### PHP文件中的Javascript和CSS代码折叠

您现在可以在PHP文件中折叠Javascript和CSS代码块，从而增强代码的组织性和可读性。

### 修复

- 修复了显示闭包的签名帮助时语言服务器崩溃的问题（[#539](https://github.com/DEVSENSE/phptools-docs/issues/539)）。
- 修复了链式方法调用后出现不必要的新行的问题 [#1969](https://community.devsense.com/d/1969-help-on-formatting-rules)

## 1.45.15260 (2024年4月8日)





### 新功能

- 补全列表显示函数签名（实验性） - 启用设置 `"php.completion.showParameters"`。
- 新增代码操作，如果适用，将 `define` 更改为 `const`。
- 修复 `string` PHPDoc 类型提示无效大小写的代码操作。
- 诊断可能错误的 `foreach` 变量。
- 设置 `"php.completion.showDeprecated"` 来控制是否在补全列表中隐藏或划线展示已弃用的符号。默认情况下这些符号被展示并划线。

### PHPUnit 测试资源管理器

测试资源管理器尊重 `#[Test]` 属性，并在列表中显示相应的测试。

### 改进

- 覆盖诊断尊重类型提示的可能 `class_alias`。
- 代码诊断下划线部分使用了trait，如果这个trait引入了不兼容的方法。
- 类型推断改进。
- 处理一些无效的 PHPDoc 类型注解。
- 更多快速代码建议。
- 优化。

### 修复

- 修复了HTML中PHP代码块的错误换行 [#1953](https://community.devsense.com/d/1953-format-html-code-in-php)
- 格式化时在 `<!DOCTYPE html>` 标签前不再引入新行 [#1940](https://community.devsense.com/d/1940-no-line-break-between-and-doctype)

## 1.45.15192 (2024年3月26日)





### 自动重命名HTML标签

现在，您可以通过单次编辑重命名php文件中的HTML标签对。通过在`settings.json`中启用`editor.linkedEditing`来开启此功能：

```json
"[php]": {
    "editor.linkedEditing": true,
}
```

### 改进

- 函数悬停信息显示泛型类型参数（如果有的话）([#1915](https://community.devsense.com/d/1915))。
- 改进在悬停提示中显示trait成员的模板类型参数。

### 修复

- 修复了`empty`、`isset`或`exit`前面不需要的空格([#522](https://github.com/DEVSENSE/phptools-docs/issues/522))。
- 修复了代码包含复杂数组初始化时可能发生的冻结问题。
- 修复了`Closure`类型参数的覆盖诊断。
- 修复了解析器以允许`namespace private;`结构。
- 修复了继承模板类型参数的类型推断问题([#503#comment](https://github.com/DEVSENSE/phptools-docs/issues/503#issuecomment-1998885037))。

## 1.45.15145 (2024年3月14日)





### 新设置

- **php.hover.parametersFullName**: 在工具提示中显示完整的类型名称（缩短为当前命名空间）。
- **phpTools.suppressPremiumFeatures**: 禁用关于高级功能的某些通知，例如代码操作。

### 重写诊断

添加了用于正确方法重写的诊断功能（[#234](https://github.com/DEVSENSE/phptools-docs/issues/234)），包括对正确使用`#[Override]`属性的检查。

此外，编辑器提供了针对常见重写错误的快速修复。

### 改进

- `.phpstorm.meta.php`中的`expectedArguments()`遵循类名范围、mixin和traits的使用。 ([#1929](https://community.devsense.com/d/1929))
- 类型推断的改进。

### 修复

- 当高级功能未激活时，自动`organizeImports`和`fixAll`不会使VSCode变慢。 ([#504](https://github.com/DEVSENSE/phptools-docs/issues/504))
- 修复了代码补全中缺失`mixed`的问题。
- 修复了一些缺失的Eloquent模型函数。
- 修复了带有`@`的条目名称的结构化数组文档注释类型。 ([#508](https://github.com/DEVSENSE/phptools-docs/issues/508))
- 修复了格式化时`return`后不必要的空格。 [#509](https://github.com/DEVSENSE/phptools-docs/issues/509)
- 修复了测试资源管理器的初始加载 ([#1934](https://community.devsense.com/d/1934))。
- 修复了`unset`语句的换行，受`callParametersWrap`选项控制。 [#518](https://github.com/DEVSENSE/phptools-docs/issues/518)

## 1.45.15061 (2024年2月27日)





### 改进

- 自动括号完成与 *IntelliPHP* 建议结合工作。
- 改进了类型推断和类型检查。
- 改进了 `foreach` 类型推断，利用泛型类型参数和 _ide_helper。
- 内联标签的 Blade 语法高亮。
- 代码格式化程序在 `.blade.php` 文件中美化 PHP 代码。
- 适用于 Eloquent 模型类的 IntelliSense。

### 重构

- 字符串连接到字符串插值重构。

### 格式化

引入了 `php.format.declCompactEmptyBody` 选项，该选项现在会自动将空函数体转换为 {} 并将其与前面的符号保持在同一行，并用一个空格分隔。

```php
function foo() {}
```

此外，我们还支持换行选项 `always`，确保始终对适当的语法结构进行换行。

### 修复

- 修复了 `.blade.php` 文件中的语义高亮问题。
- 在添加/删除 `"php.stubs"` 或在 `composer.json` 的 `require` 中添加/删除 `ext-**` 后更新问题。
- 实现接口或抽象的代码操作添加了正确的类型提示。
- 修复了罕见的语言服务器崩溃（内存不足、100% CPU 和崩溃）。
- 修复了函数名称后不希望出现的空格，这些名称恰好也是关键字 [#1481](https://community.devsense.com/d/1481-space-after-if-as-a-formatting-rule)。
- 修复了完全不起作用的格式化问题。

## 1.44.14997 (2024年2月14日)




### 改进

- 改进了混合PHP、HTML/CSS/JS代码的格式选择，改善了`editor.formatOnType`和`editor.formatOnPaste`行为。
- 支持`@psalm-yield`文档注释标签，并据此推断`yield`的结果类型。
- 针对`#[Override]`属性的诊断。
- 支持phpdoc类型`trait-string`、`interface-string`、`enum-string`、`callable-string`。
- 支持`phpcs:ignore`注释。

### 工具提示改进

- 工具提示显示更短的类型名称（可以通过设置`"php.hover.parameters.fullname"`进行更改）。
- 签名帮助工具提示在适当时显示`never`返回类型。
- 修复了`class-string`类型提示。

### 修复

- 在HTML注释内正确突出显示刀片标签。
- 修复了函数重写的自动完成问题。
- 修正了在行注释前的多行表达式部分的错误缩进。
- 避免访问变量作为数组时产生错误的`6404`诊断。
- 当文件更改时更新相关诊断到其他文件。
- 稳定性修复。

## 1.44.14950 (2024年2月7日)





### 改进

- 在输入 `default:` 或 `case ... :` 后自动进行格式化。
- 改进了函数签名的鼠标悬停功能，提供更详细的 `array` 类型规格。
- 改进了对 `array_rand()` 和 `is_array()` 的类型推断。
- 修复了在 PHP 代码中使用 `{{` 的问题。
- 支持更多的 Laravel Blade 标签（`@extends`、`@can`），修复了 blade 标签中的语法错误。

## 1.44.14925 (2024年2月5日)





### Laravel Blade 编辑器

此更新启用了 Laravel Blade 标签内 PHP 语法的实验性着色功能：
- 着色 `{{`/`}}`、`{!!`/`!!}`、`{{{`/`}}}`、`@php`/`@endphp` 内的代码
- 着色 Blade 标签表达式内的代码，例如 `@if ( ... )`
- 着色 blade 标签
- 着色 blade 注释，例如 `{{-- ...  --}}`

此外，所有嵌套的 PHP 代码将获得标准功能，包括 **IntelliSense**、**诊断**、**代码操作**、**代码修复**、**工具提示** 等。

![blade editor colors](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-blade-colorization.png)

### 改进

- 在应用代码操作或代码修复后自动格式化代码。
- 改进对内置 `array_*` 函数的数组类型分析。
- 了解更多前缀为 `@psalm-` 的文档块标签，例如 `@psalm-property`，`@psalm-readonly`，`@psalm-trace`，等等。
- 对于文档块标签 `@trace` 或 `@psalm-trace`，提供内嵌提示和变量高亮。
- `.blade.php` 文件的整体解析器改进 - 支持 `@php` 和 `<?php` 块，支持大多数文档的 blade 标签和块。
- 支持 `never` 返回函数、函数 _退出_，以及总是抛出异常的函数。
- 当有可用的代码操作时显示三点。

### 代码操作

- 如果可能，快速将 `if` 重构为 `switch`。
- 删除不必要的括号，并将其变暗。

### 格式化

我们更改了直接在 switch 条目中存在的大括号的默认缩进行为。[#1897](https://community.devsense.com/d/1897-custom-formating-rules)

### 修复

- 修复了一个问题，该问题可能导致包含 PHP 和 HTML 元素混合的复杂文件的格式化程序缩进不正确。[#1881](https://community.devsense.com/d/1881-autoformat-on-save)
- 修复了类常量使用之前的注释缩进不正确的问题 [#476](https://github.com/DEVSENSE/phptools-docs/issues/476)
- 修复了部分 CSS 选择器由 PHP 生成时的格式化问题 [#1736](https://community.devsense.com/d/1736-auto-formatting-error-in-css)
- 修复了 `never` 返回函数的工具提示。
- 修复了函数参数中的属性缩进不正确的问题 [#1899](https://community.devsense.com/d/1899-autoformat-attributes-indentation-in-function-parameters)
- 修复了格式化特定情况下不必要的换行移除 [#1895](https://community.devsense.com/d/1895-php-formatting-issue)
- 稳定性修复。

## 1.43.14858 (2024年1月24日)




### 不必要的括号

可以安全移除的括号现在在代码中被淡化显示，并且提供了相应的代码修复"移除不必要的括号"。

### 改进

- 从lambda返回类型推断的泛型参数的类型推断。
- 格式化器处理注释中的 `@formatter:off` 和 `@formatter:on` 指令。

### 格式化

根据用户的反馈 [#395](https://github.com/DEVSENSE/phptools-docs/issues/395)，我们为Joomla开发者添加了新的代码风格！要启用它，请将 `"php.format.codeStyle"` 设置为 `"joomla"`。

### 修复

- 修复了 `"drupal"` 的代码风格（`"php.format.codeStyle"`设置），插入空格。
- 修复了 `::` 运算符后的自动完成。
- 避免在键入新数组 `[` 时触发自动完成...
- 修复了在 `case` 标识符后的不需要的空格 [#469](https://github.com/DEVSENSE/phptools-docs/issues/469)
- 修复了当数组有两个空字符串时不正确的出现高亮显示。
- 内存和性能改进。
- 修复了导致恒定CPU使用和_ devsense.php.ls _进程永无止境的问题。

## 1.43.14756 (2024年1月15日)





### `$_SERVER` 和 `$GLOBALS` 的代码补全

代码补全为 `$_SERVER` 和 `$GLOBALS` 超全局变量提供已知数组键。类型推断也将它们纳入考虑。

![$_SERVER items completion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-server-var-completion.gif)

### 数组键的代码补全

尽可能列出和补全数组键。这对于结构化数组文档注释（如 `array{name:string,id:int}`）和数组初始化器（如 `new ['name' => "John, 'id' => 1]`）效果很好。

### 代码操作和重构

- 生成构造函数属性的 getter/setter 的代码操作。
- 简化 `isset(A) ? A : B` 的代码操作。

### 改进

- 支持包含多行 `array<>` 语法的文档块。
- 支持使用 `=` 字符的 `@psalm-type` 定义的文档块。
- 处理定义整个表达式类型（而不仅仅是变量）的 `@var` 文档块。
- 改进在存在大量具有键名的数组类型时的类型分析。
- 处理 `instanceof` 操作符复杂左值的类型分析。
- 改进在存在大量具有键名的数组类型时的类型分析。
- 改进 `??` 操作符的类型分析。
- 改进在 WordPress 源代码中处理全局变量。
- 数组键的代码补全、数组条目的类型推断，并在 `[` 后触发补全。
- 对通过引用 (`&`) 的变量和表达式类型的内联提示不会在双击时插入。
- PHP 语言级别在未设置特定 `php.version` 时遵循 `composer.json`。

### 格式化

- 基于用户请求实现的链式方法调用换行（[#1868](https://community.devsense.com/d/1868-new-line-after-method-chaining)）。目前，此设置仅允许使用 `always` 选项。
- 添加了在方法链换行应用时指定分号在新行上的位置的功能。

### 调试

我们添加了 `maxConnections` 启动设置来控制同时调试会话的最大数量。[#353](https://github.com/DEVSENSE/phptools-docs/issues/353)

### 修复

- 修复了方法名中 `do` 后出现意外空白的问题。[#1871](https://community.devsense.com/d/1871-unexpected-white-space-after-function-name)
- 修复在 Symfony 框架中出现的堆栈溢出异常的稳定性问题。[#437/46](https://community.devsense.com/d/437-stack-overflow-in-symfony-project/46)

## 1.42.14626 (2023年12月30日)





### 改进

- 改进了 `array_unshift()` 类型分析。
- `private` 属性的重构。
- 在 `property_exists()` 函数内指定的属性名称重构。
- 改进对快捷本地作用域的检测和补全。
- WordPress 的结构化数组/对象文档注释语法能够被代码分析和代码补全识别并遵守。
- 带有内联描述的 `@var` 注释变量的工具提示。
- 为 `_ide_helper.php` 中错误生成的类型名提供诊断。
- 对 `${}` 弃用字符串插值进行诊断以及相应的代码操作。
- 对多余的 `?>` 关闭标签进行诊断以及相应的代码操作。

### 修复

- 更新了 PHP 解析器以处理 PHP8+ FQN 命名空间语法中的关键词。
- 修复了从 `ftp://` 远程使用某些FTP扩展打开工作区时的启动问题。
- 修复了错误的无法到达代码的诊断。
- 如果使用 `property_exists()` 检查了属性，则不报告未知属性。
- 修复了在模糊函数调用中（函数定义在两个位置或在两个文件中打开）的 _内嵌提示_。
- 修复了崩溃问题。

## 1.42.14434 (2023年12月12日)





### PHP Stubs 用户界面

添加了一个快速命令 `> Workspace Stubs`，可以快速选择存根（包括 PHP 书籍和其他存根如 `"WordPress"`），以便在 IntelliSense 和代码分析中使用。

![PHP Stubs UI](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-php-stubs-ui.png)

### `"source.fixAll"` 操作

安全的快速修复，例如简化名称，可以在文件保存时自动修复。使用以下设置可以在文件保存时应用安全的快速修复：

```json
"editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
}
```

### 调试

#### 断点解析

通过 Xdebug 的信息验证断点位置，提高了断点解析。具体如下：

- 已绑定的断点以红色突出显示。
- 未绑定的断点以灰色视觉区分。
- 在无法绑定到断点附近的有效位置时，断点将自动调整到有效位置。

#### xdebug_notify 支持：

增加了对 `xdebug_notify()` 的支持，能够将信息和对象发送到调试控制台。此功能通过直接向控制台传递相关数据，增强了调试体验。

#### 错误和警告

我们已实现将 PHP 警告和错误输出到调试控制台的方法。这种方法为开发人员提供了一个集中位置，以在调试会话中监控和解决问题。

### 改进

- **快速修复** 缺失的 `use` 函数。
- 为 `newrelic` 添加了 **`php.stubs`**。
- 隐式将来自 `composer.json` 的 **PHP stubs** 包含到 IntelliSense 和代码分析中。
- **更复杂的 PHP 可执行文件**：这允许使用远程 `php`，或自定义命令来运行 `php`。设置 `php.executablePath` 或 `php.executables` 可以包含带参数的命令（即 `ddev exec php`）。**注意：**现在可能需要双引号。
- **PHPUnit 路径可以是绝对路径**：将设置 `phpunit.phpunit` 放入双引号中，以保持自定义 phpunit 路径不变，即 `"phpunit.phpunit": "\"phpunit\""`。
- **PHPUnit 命令可以自定义**：使用新设置 `phpunit.command` 可以完全自定义运行 PHPUnit 的命令。使用变量自定义命令：
    - `${cwd}`: 工作区根路径，本地。命令将在此目录中执行。
    - `${phpunit}`": phpunit 二进制文件的路径。它会自动解析或可以通过 `phpunit.phpunit` 设置自定义。
    - `${phpunitxml}`: 相对于工作区根目录的 phpunit.xml 路径。
    - `${phpunitargs}`: 构建的 PHPUnit 参数。(我们需要 --teamcity 和 --filter 以正常工作)
    - `${phpargs}`: 确保 PHP 正确运行和调试所需的可选参数。

### 格式化

为了响应您的反馈([source](https://community.devsense.com/d/1792-turn-off-codelens/8))，我们实施了两个额外的选项，以提升代码格式的灵活性：

#### 保持函数在单行

引入了 `php.format.rules.keepFunctionsOnOneLine` 选项，允许用户指示格式化器在函数或方法位于单行时不进行换行。这使开发人员能够保持简洁和一致的编码风格。

#### 保持类在单行

通过新的 `php.format.rules.keepClassesOnOneLine` 选项，您现在可以在类位于单行时防止格式化器换行。此功能支持维护代码库的简洁和紧凑结构。

### 修复

- 修复代码操作以在全局命名空间中排序和移除 `use`。
- 改进了返回 `static`/`$this` 的方法的解析 ([#1820](https://community.devsense.com/d/1820))。
- 在编辑接近嵌入提示位置的代码时修复了它们的位置。
- 修复了测试资源管理器中的“转到源”功能。
- 当更改可能存在风险时，重命名重构显示 _预览_。
- 重命名重构正确处理构造函数的属性 ([#450](https://github.com/DEVSENSE/phptools-docs/issues/450))。
- 各种代码分析改进。
- 针对各种 `_ide_helper.php` 错误的解决方法。
- 修复了条件断点的问题。之前的版本在某些情况下破坏了此功能。
- 修复了实现带有 `static` 函数的接口的代码操作 ([#446](https://github.com/DEVSENSE/phptools-docs/issues/446))。
- 修复了嵌套关联数组中多函数的错误格式化问题 ([#432](https://github.com/DEVSENSE/phptools-docs/issues/432))。
- 修复了使用旧版 Xdebug 启动调试器时的 `无效或缺少选项` 警告 [#1816](https://community.devsense.com/d/1816-all-in-one-php-support)

### 高级功能

- 注：_代码操作_ 和 _代码修复_ 可在 [PREMIUM](https://www.devsense.com/en/purchase) 中使用。此更新之前可能未获得许可状态下无意中工作。

## 1.41.14263 (2023年11月14日)





### 格式改进

#### 注释

在此更新中，我们改进了对注释的处理方式。现在，表达式后的注释会保留在其原始位置，用户可以根据需要灵活调整缩进。

```php
$x = [
  1  => 'one'      // 第一个注释
  42 => 'fortytwo' // 第二个注释
]
```

#### 对齐匹配分支主体

格式化程序现提供“对齐匹配分支主体”功能，以在 `match` 表达式中对齐主体（结果），增强代码清晰性和结构。您可以通过 `php.format.rules.alignMatchArmBodies` 选项启用此功能。

```php
match ($day) {
    'Monday'    => 'Work',
    'Tuesday'   => 'Tacos',
    'Wednesday' => 'Waffles'
};
```

### 文档注释和类型注解

- **结构化 `object` 类型**：可以在文档注释中使用 `object{property:type,}` 语法动态注解对象。

- **全局 `@type` 别名**：类型别名可以在整个文件范围内使用文档注释 `@type`、`@phpstan-type`、`@phpstan-import-type`、`@psalm-type`、`@psalm-import-type` 定义。以前，它仅适用于类和函数上方。现在，在全局文件范围内的任何地方的文档注释 `/** */` 中也有效。

- 文档注释中合格名称的**代码操作**（[#428](https://github.com/DEVSENSE/phptools-docs/issues/428)）

- 支持带修饰符的 **@method** 语法，即 `@method public static foo()`。这是一种不常见的语法，但我们现在理解它了。

### `redis` 存根已添加

可以将 `"redis"` 添加到您的 `"php.stubs"` VSCode 设置中。这增加了对使用 `redis` 扩展的类型检查和 IntelliSense 支持。

### 重命名预览中的诊断

在使用**预览**重命名符号时（`F2`，`Shift+Enter`），预览窗口会进行分析并下划线显示错误和警告。

### 调试

#### 随机 Xdebug 端口

目前，在 `launch.json` 中指定 `"port": 0` 被视为一个随机可用端口。`php` 会自动使用对应的 `xdebug.port = ${port}` 指令启动。默认情况下，如果您没有指定任何内容，端口已经是随机选择的。大多数**运行和调试**命令现在都能正常工作。

示例启动配置，将启动_内置 Web 服务器_、启动调试并打开浏览器：

```json
{
    "name": "Launch Built-in server",
    "type": "php",
    "request": "launch",
    "runtimeArgs": ["-S", "localhost:8888", "-t", "public"],
    "port": 0,
    "serverReadyAction": {
        "action": "openExternally"
    }
}
```

您也可以完全省略 `"port": 0,`，因为它是此启动配置的默认值。

> 注意，当仅_监听 Xdebug_时，默认端口仍为 `[9003, 9000]`。

> 更多信息请参阅：https://docs.devsense.com/en/vscode/debug/launch-json#built-in-php-server

快捷启动命令（不需要 `launch.json` 文件，只需按 `F5`）也使用随机可用的 Xdebug 端口。您无需做任何操作。

#### 表达式评估增强

现在，可以在各种上下文中将表达式展开到更深的层次，包括调试控制台和监视窗口。享受改进的评估结果带来的增强调试体验。

#### 运行/调试当前 PHP 文件

现在，您可以使用编辑器右上角的快速运行/调试按钮运行或调试当前打开的 PHP 文件。

### 修复

- 修复了换行行为，确保当注释在表达式后时保持在原始行。[#1760](https://community.devsense.com/d/1760-php-format-codestyle-psr-12-makes-my-comments-borken)
- 修复了 `php.inlayHints.parameters.suppressNameMatchingValue` 设置。
- 修复了应用“实现抽象”代码操作后的代码缩进。
- 修复了 `enum` 中的 `use` 代码操作。[#425](https://github.com/DEVSENSE/phptools-docs/issues/425)
- 修复了在浏览器中运行的**web**扩展（[vscode.dev](https://vscode.dev)）。
- 修复了在命名空间中处理 `@see` 标签时的导航和自动完成功能。
- 修复了 LS 崩溃（堆栈溢出）。[#427](https://github.com/DEVSENSE/phptools-docs/issues/427)
- 修复了在属性提升中 `readonly` 和类型之间不必要的空格移除问题。[#433](https://github.com/DEVSENSE/phptools-docs/issues/433)
- 改善了在符号声明有歧义的情况下鼠标悬停提示 。

## 1.40.14103 (2023年10月18日)





### 引入 IntelliPHP 🚀

我们很高兴地宣布，PHP 扩展现在捆绑了 **[IntelliPHP](https://marketplace.visualstudio.com/items?itemName=DEVSENSE.intelli-php-vscode)**。

![IntelliPHP](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/intelliphp-vscode.gif)

**IntelliPHP**: _您的本地 PHP AI_ - 在您输入时实时提供整行建议。使用 `TAB` 键完成建议，提高工作效率！[阅读更多 ...](https://blog.devsense.com/2023/php-and-visual-studio-updates-july-2023)

### 次要功能

- `"php.inlayHints.insertOnDoubleClick"` 设置，用于启用或禁用双击时插入嵌入提示 ([#1717](https://community.devsense.com/d/1717))。
- `array_multisort()` 不再将第一个参数视为严格按引用传递 ([#1729](https://community.devsense.com/d/1729))。
- 改进的文件路径跳转和代码补全 ([#1735](https://community.devsense.com/d/1735))。
- 工具提示中的 `@see` 和 `@exception`。
- `list{}` 文档注释形状。

### 格式化

格式化器支持新的 **PHP 8.3** 语法。

### 末尾新行

默认情况下，格式化器将不再裁剪末尾新行。末尾新行将保持原样。然而，如果您启用了 `files.insertFinalNewline` 且缺少末尾新行，格式化器将自动为您添加。

### 修复

- 修复了在 **code-server** 和 GitHub CodeSpaces 上的安装问题。
- 修复了包含递归符号链接的 `vendor` 文件夹 ([#1720](https://community.devsense.com/d/1720))。
- 当方法接受可变参数时，修正了错误的命名参数错误 ([#1722](https://community.devsense.com/d/1722))。
- 修复了可能的堆栈溢出和语言服务器崩溃 ([#1724](https://community.devsense.com/d/1724))。
- 修复了生成器返回类型的分析。
- 修复了以关键字作为命名参数时不正确的格式化 [#408](https://github.com/DEVSENSE/phptools-docs/issues/408)
- 修正了构造函数内的错误缩进 [#409](https://github.com/DEVSENSE/phptools-docs/issues/409)

## 1.39.13943 (2023年9月20日)





### 类名内联建议

现在，当输入一个新类时，会根据文件名建议类名。此建议利用了 Visual Studio Code 的内联完成 UI，因此不会造成干扰；可以使用 `TAB` 键接受。

![PHP class name suggestion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-complete-class-name.gif)

结合 [IntelliPHP](https://marketplace.visualstudio.com/items?itemName=DEVSENSE.intelli-php-vscode)，内联代码建议更加详细和强大！

### 补全文件路径

从此次更新起，编辑器支持补全并导航到文件 [#402](https://github.com/DEVSENSE/phptools-docs/issues/402)。

![file path suggestion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-complete-filenames.gif)

### 修复

- 支持旧式 `composer/installed.json` 文件。
- 修复了一些在 PHP 与 HTML 混合时出现的格式问题。

## 1.38.13918 (2023年9月15日)





### Getter/Setter 命名约定设置

添加了用于生成getter和setter命名约定的设置。

![set naming convention](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/getterSetterNaming.png)

### PHP 8.3 语法

添加对 **PHP 8.3** 语法特性的支持，包括：

- 类型化类常量
- 匿名只读类
- 动态类常量获取

### 格式化

响应用户反馈([#384](https://github.com/DEVSENSE/phptools-docs/issues/384), [#1691](https://community.devsense.com/d/1691-array-trailing-commas), [#684](https://community.devsense.com/d/684-code-format-array-last-item-comma))，我们引入了额外的格式化选项，允许用户精确控制在PHP代码中自动放置逗号的方式。

这些新选项包括：
 - `php.format.rules.addCommaAfterLastArrayElement`: 在数组的最后一个元素后添加逗号。
 - `php.format.rules.addCommaAfterLastCallParameter`: 在函数调用的最后一个参数后添加逗号。
 - `php.format.rules.addCommaAfterLastDeclParameter`: 在函数或方法签名中最后一个声明的参数后添加逗号。

除了上述选项，我们还引入了以下格式化选项：
 - `php.format.rules.booleanConstantCasing`: 定义 `true` 和 `false` 常量的大小写。
 - `php.format.rules.nullConstantCasing`: 定义 `null` 常量的大小写。

### 修复

- 调试器处理带 `%` 字符的文件路径 [#380](https://github.com/DEVSENSE/phptools-docs/issues/380)
- 修复 /vendor/ 缓存问题
- composer 更新后问题得到更新
- 内存使用优化
- 避免在不是关键字的情况下显示关键字工具提示
- 避免在查看窗口中显示重复项
- 使用Drupal代码风格时，格式化器将所有 True/False/Null 常量更改为大写。[#870](https://community.devsense.com/d/870-drupal-code-style-doesn-t-do-uppercasing-true-false-null)
- 同时对格式化或嵌入式提示的设置进行多次更改时，仅考虑第一个更改；后续更改被忽略。
- 解决了与PSR-12编码标准相关的格式化问题，对于多行参数列表，关闭括号和打开大括号现在按照PSR-12标准正确地放在同一行，并在它们之间留有一个空格。
- 更多的代码诊断和IntelliSense修复。
- 数组初始化值现在以增加的缩进级别格式化。[#935](https://community.devsense.com/d/935-format-indent-array-initializers-values)
- 修复与多行数组初始化器相关的其他格式化问题。
- 稳定性修复。

## 1.38.13779 (2023年9月1日)




### 修复

- 粘性滚动 [#387](https://github.com/DEVSENSE/phptools-docs/issues/387)
- `default` 情况的工具提示 [#1692](https://community.devsense.com/d/1692)
- 属性的工具提示
- 修复未指定类型参数的类型分析
- 修复问题分析设置
- /vendor/ 的缓存修复
- 修复在 /vendor/ 文件中使用 `static` 的问题 [#389](https://github.com/DEVSENSE/phptools-docs/issues/389)
- 修复在工作区中错误创建的临时缓存 [X/1697612088196137243](https://twitter.com/driesvints/status/1697612088196137243)

## 1.38.13759（2023年8月30日）





### 优化加载和内存使用

在此更新中，我们开始缓存带有`vendor`文件夹的`composer.lock`。这显著改善了基于Composer包的工作区打开速度，并将RAM使用降至最低限度。

_对于我们的内部人员_，请查看您的`OUTPUT` / `PHP Language Server`面板以了解其操作情况。

### 属性的嵌入提示

新增功能，类上方的属性将会有带参数名称的嵌入提示（[#383](https://github.com/DEVSENSE/phptools-docs/issues/383)），如果已启用。

### `scalar_objects` 支持

感谢建议 [#378](https://github.com/DEVSENSE/phptools-docs/issues/378)，我们添加了对Nikita Popov的[`scalar_objects`](https://github.com/nikic/scalar_objects)扩展的原生支持。

编辑器会识别`register_primitive_type_handler()`调用，并允许对指定标量类型进行补全。

### 格式化

直接响应[用户请求](https://community.devsense.com/d/1656-line-up-on-consecutive-constants)，我们添加了格式化选项以对齐常量 `php.format.rules.alignConstants` 和枚举情况 `php.format.rules.alignEnumCases`。现在保持对齐一致变得轻而易举：

```php
class X {
    const a   = 1;
    const bb  = 2;
    const ccc = 3;
}
```

### 虚拟文件的代码分析

我们已为虚拟文件（例如差异视图、预览、git预览等）启用了完整的代码分析。这使您可以轻松分析即将提交的更改！

![analyse virtual document](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-analysis-virtual-document.png)

### 具有符号详细信息的大纲

感谢建议 [#109](https://github.com/DEVSENSE/phptools-docs/issues/109)，我们已向文档大纲添加了更多详细信息。它显示方法访问、类访问以及`interface`、`trait`、`enum`类型。

![Symbol outline with details](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/outline-with-details.png)

### 修复

- 修复关闭VS Code或工作区时的延迟。
- 修复`use`语句排序问题。
- 修复在`trait`中定义的方法的转到定义功能。
- 修复`@psalm-import-type` phpdoc标签支持。
- 修复在没有参数的情况下出现`new`时的嵌入提示。
- 修复静态方法的重命名重构。
- 优化。
- 修复在命名空间中使用保留字时发生的格式化问题，如default。

## 1.37.13534 (August 4, 2023)





### 补全命名空间标签

现在，代码补全在类名旁边显示命名空间。此功能默认**启用**，可以通过 `"php.completion.showNamespaceLabel"` 设置进行控制。

![completion namespace label and colored tool tips](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/color-completion-and-namespace-label.png)

### 补全着色详情

代码补全弹出窗口也进行了格式化和着色。

### IntelliSense

- 已添加单引号字符串中的类名补全。

### 修复

- 修复了无限内存使用的问题（[#343](https://github.com/DEVSENSE/phptools-docs/issues/343#issuecomment-1664221959)）
- 修复了数组未自动对齐的问题 [#364](https://github.com/DEVSENSE/phptools-docs/issues/364)
- 修复了重复警告。
- 在折叠 HTML 标签时，关闭标签保持可见。[#363](https://github.com/DEVSENSE/phptools-docs/issues/363)
- 修复了变参移除空格的问题 [#1639-2](https://community.devsense.com/d/1639-wrongly-detected-problems-for-constructor-arguments/2)
- 解决了多个关于 HTML 标签与 PHP 标签嵌套和组合的问题。[#1634](https://community.devsense.com/d/1634-indentation-problems-with-auto-format-in-vs-code)

## 1.36.13417 (2023年7月1日)




### 调试器 &amp; `trigger` 设置

新的启动设置 `"trigger"` 允许控制是调试还是忽略某些请求。

```json
{
    "name": "Debug built-in server",
    "type": "php",
    "request": "launch",
    "runtimeArgs": [
        "-S",
        "localhost:8000",
        "-t",
        "./public"
    ],
    "trigger": "THIS",
},
```

以上的 `launch.json` 设置将启动内置 Web 服务器，配置所有 Xdebug 指令，并等待请求。只有带有 `GET` 参数 `XDEBUG_TRIGGER=THIS` 的请求会被调试。任何其他请求将被调试器忽略。即，请求 `http://localhost?XDEBUG_TRIGGER=THIS` 将启动调试，而 `http://localhost` 则不会。

### IntelliSense 和 `IteratorIterator`

`IteratorIterator` 和 `RecursiveIteratorIterator` 扩展了泛型类型参数 `TInner`、`@mixin TInner`，并且它们的 `__construct()` 会推断这个 `TInner`。因此，IntelliSense 知道内部迭代器类型，可以提供内部迭代器的成员。 ([#1613](https://community.devsense.com/d/1613))

### 新的 IntelliSense 功能

- 支持 `@phpstan-type` 和 `@phpstan-import-type` ([#1543](https://community.devsense.com/d/1543-local-type-aliases))。
- 在包含目录中处理 `phpstan.neon`（和 `.dist` 替代品）；支持其全局类型别名（`phpstan.neon` 文件的 [`"typeAliases"`](https://phpstan.org/writing-php-code/phpdoc-types#global-type-aliases) 设置）。
- 正确处理 `Collection<TValue>`、`Iterator<TInner>`。
- 使用魔术 `__get()` 访问的未定义属性报告为较低的严重性。
- 修复了特征适配和类继承分析。拥有复杂继承以及带有适配的特征 `use` 的类被正确分析，提供关于缺失方法实现的有用见解。
- 修复了某些 `try`/`finally` 块的控制流分析。
- 提升了 Laravel 的 IntelliSense。

### 命名空间自动导入

已经存在的命名空间自动导入功能，可以在使用代码补全时无缝添加相应的 `use` 或完全限定的名称。还提供代码操作，你可以选择一个新的命名空间进行导入。此外，我们正在添加命令 `Import class ...` 和 `Fqn class ...`，以使用命令栏 (`F1`) 和快速选择窗口导入命名空间 ([#450](https://community.devsense.com/d/450))。

### 稳定性修复

- 修复了解决方案中存在 `.phar` 文件时的内存泄漏问题。

## 1.35.13327 (2023年6月20日)





### 组织使用

现在可以在源代码中的任何地方调用名为_整理导入_的操作（[#349](https://github.com/DEVSENSE/phptools-docs/issues/349)）。移除和排序`use`语句会影响整个代码块，而不仅仅是单行。

### Composer

可以使用设置`composer.bin`显式设置`composer.phar`的路径。此外，解析`composer.phar`得到了改进，因此它大多数情况下会使用您已经安装的composer。否则，如果用户没有安装composer，它会被自动下载并使用，无需任何操作。

### 重构

在语义高亮、查找引用、方法重写的代码透镜及重命名重构中解析Trait函数成员。

### 调试器 &amp; Phar

扩展程序现在解析并理解 `.phar` 文件。自此更新以来，可以在 `.phar` 文件内进行代码调试和逐步执行。Phar文件被解码、打开，当前语句会像一个普通的 `.php` 文件一样高亮显示。本地变量也可以被检查，并且内联调试值也可以正常工作。

### 稳定性

此更新修复了与`code`被关闭时进程未能终止相关的问题。

## 1.34.13295 (2023年6月15日)





### IntelliSense &amp; `@phpstan-type` 和 `@psalm-type`

从现在起，我们开始支持本地类型别名的基本功能。

### IntelliSense &amp; 带泛型的Traits

新增功能，现在可以通过`@use`文档注释为`trait`使用指定泛型参数 ([#840](https://community.devsense.com/d/840-generics-allow-template-for-trait-usages))，例如：

```php
class MyClass {
    /** @use MyTrait<int, string> */
    use MyTrait;
}
```

### IntelliSense &amp; `static` 类型

我们重新实现了内部机制，并改进了涉及到在traits中使用`static`和`$this`、受保护的属性和类继承的多种情形的类型分析。此外，通过更多的继承类型信息，我们更好地解析了泛型参数和trait成员 ([#931](https://community.devsense.com/d/931-inherit-and-static-array-type/))。

### PHPUnit 测试 &amp; 自动运行

新增功能，现在可以自动连续运行测试。在*Testing*面板中的*watch*图标允许保持所有测试、测试套件或仅特定测试用例始终为最新状态。 ([#1479](https://community.devsense.com/d/1479-autorun-test-suite-on-file-save))

### 次要改进

- 命名参数的代码补全在结尾补全`:`。 ([#1600](https://community.devsense.com/d/1600-improved-autocomplete))
- 带提示的数组键在单引号内的代码补全。 ([#1600](https://community.devsense.com/d/1600-improved-autocomplete))
- 在键入`instanceof`关键字后按下SPACE后触发代码补全。

### 修复

- 修复了几个内存泄露！
- 在合格名称内不再将`match`、`fn`和`interface`报告为语法错误（PHP 8.0+）。 
- PHP 8.2 独立的`true`、`false`和`null`类型名称。 ([#338](https://github.com/DEVSENSE/phptools-docs/issues/338))
- 修复了一些类型推断的情况。
- 修复了将带`@ignore`标记的函数报告为未知的问题。
- 修复了在`if`之上通过`/** @var */`进行的类型提示。
- 修复了`define()`的检查。 ([#340](https://github.com/DEVSENSE/phptools-docs/issues/340))
- 修复了在抽象方法之后格式化时移除新行的问题。 [#1525](https://community.devsense.com/d/1525-formatting-issue)
- 箭头函数现在遵循php.format.rules.spaceWithinDeclParens以在括号内添加空格。 [#1536](https://community.devsense.com/d/1536-space-within-fn-parenthesis)
- 修复了函数名称为关键字时的多余空格 [#335](https://github.com/DEVSENSE/phptools-docs/issues/335)
- 如果前一个兄弟节点在同一行结束，不要增加缩进 [#333](https://github.com/DEVSENSE/phptools-docs/issues/333)
- 修复了当键不是简单文本时数组项对齐的问题 [#1602](https://community.devsense.com/d/1602-auto-format-woes)

## 1.34.13120 (2023年5月5日)




### 智能感知

#### Trait 适配块

在 `trait` 适配块中实现了代码补全和工具提示。([#582](https://community.devsense.com/d/582))

#### 其他改进

- 在 `is_a()` 的上下文中类型推断得到正确分析。
- 如果存在 `__callStatic()` 魔术方法，则静态调用的非静态方法减少了虚假警告。
- 新的代码操作快速重构。
- 更新了集成的 PHP 手册和本地化。

### 添加缺失的 PHPDoc

`添加缺失的 PHPDoc` 代码操作将文档注释作为片段插入 ([#157(comment)](https://github.com/DEVSENSE/phptools-docs/issues/157#issuecomment-1512313864))。这替换了模板变量，并允许您在占位符中输入。

### 格式化

我们添加了一个选项，允许您在指定的代码范围内打开或关闭格式化。在注释 `// @php-format off` 或 `/* @php-format off */` 和对应的注释 `// @php-format on` 或 `/* @php-format on */` 之间的代码将不会被格式化。

此外，我们还添加了一个新选项 `php.format.rules.declKeepRightParenAndOpenBraceOnOneLine`，它将在函数或方法声明头的右括号 `)` 和主体的开括号 `{` 保持在一行。

其他允许进行更多格式调整的选项包括：
- `php.format.rules.openBraceOnNewLineForNamespaces` 将命名空间声明的开括号 `{` 放在新行上。
- `php.format.rules.openBraceOnNewLineForBlocks` 将所有类型代码块的开括号 `{` 放在新行上，除非其他格式规则控制。
- `php.format.rules.spaceBeforeParenthesesInControlStatements` 在控制语句的括号前插入空格。
- `php.format.rules.spaceBeforeParenthesesInCalls` 在方法、函数和构造函数调用的括号前插入空格。
- `php.format.rules.spaceBeforeParenthesesInDeclarations` 在方法、函数和构造函数声明的括号前插入空格。

### 内联提示

我们添加了一个选项，仅为命名函数显示返回类型内联提示，而不用于匿名函数和箭头函数 ([#326](https://github.com/DEVSENSE/phptools-docs/issues/326))。

### 修复

- 在类型检查和类型推断检查中尊重 `class_alias()`。
- 尊重 `@return $this` 并将其视为 `static` 返回类型提示。
- 在生成函数的 **PHPDoc** 时，尊重 `"php.completion.autoimport-docblock"` 设置 ([#896](https://community.devsense.com/d/896))。
- `"mongodb"` 存根更新并修复了一些缺失的 MongoDB 类和函数。使用设置 `"php.stubs": {"*", "mongodb"}` 来使用它 ([#927](https://community.devsense.com/d/927))。
- 如果需要，查找所有引用执行类型分析以提供更好的结果 ([#322](https://github.com/DEVSENSE/phptools-docs/issues/322))。
- 修复了使用 PHPDoc `@method` 标签引入的命名参数的方法 ([#921](https://community.devsense.com/d/921))。
- 正确处理可空的 `?static` 类型。
- 代码诊断的改进，避免一些虚假警告。
- 修复在完成用户片段时的内部错误。
- 当多行 PHP 代码存在于 JavaScript 字符串内时，格式化未正确工作 [#908](https://community.devsense.com/d/908-tab-stop-indentation-with-open-curly-braces/5)。
- 修复在多行静态函数调用中使用命名参数时的不正确缩进。
- 修复当使用多个 foreach 冒号块时不必要的换行压缩 [#893-12](https://community.devsense.com/d/893-another-formatting-issue/12)。
- 修复在某些情况下命名参数的错误缩进 [#928](https://community.devsense.com/d/928-wrong-formatting-of-named-arguments)。
- 修复伪类常量的不正确缩进 [#932](https://community.devsense.com/d/932-formatting-issue)。
- 修复 PHP 在 script/style 标签内的格式化问题 [#1460](https://community.devsense.com/d/1460-codeigniter-4)。
- 修复用 `/*` 分隔的多行注释中缩进丢失的问题 [#1489](https://community.devsense.com/d/1489-code-formatting-issue-in-visual-studio-code-using-php-tools/3)。
- 修复格式化移除 `/*` 注释中的空行 [#1522](https://community.devsense.com/d/1522-comment-block-issue)。
- 修复多重嵌套多行 lambda 函数的不正确缩进 [#1500](https://community.devsense.com/d/1500-formating-issue)。

## 1.33.12934 (2023年4月8日)




### IntelliSense

现在支持 `.phpstorm.meta.php` 中的 `expectedArgments()` 和 `argumentsSet()`。

![expectedarguments](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/meta-expectedarguments.png)

### 修复

- 修复了格式化时在箭头或 lambda 函数后压缩空格的问题（[#913](https://community.devsense.com/d/913-after-update-formatting-deletes-empty-lines-and-moves-curly-braces-up)）。
- 修复了在导航到定义（“转到定义”命令）时的内部异常。
- 修复了在 Drupal 中大型文件中的罕见崩溃情况。
- 在代码补全的函数体中添加了缺失的 `static` 关键字。
- IntelliSense/代码分析处理 `iterable<K,T>`（具有 2 个泛型参数）方式与 PHPStan 相同（[#914](https://community.devsense.com/d/914-generic-of-traverable/2)）。

## 1.33.12924 (2023年4月5日)





### 测试资源管理器

_测试资源管理器_ 会查找和监视任何符合全局模式 `**/phpunit*.xml` 或 `**/phpunit.xml.dist`（不在 `vendor` 文件夹中）的 _PHPUnit_ XML 配置文件 [#313](https://github.com/DEVSENSE/phptools-docs/issues/313)。这允许在同一目录中使用自定义名称拥有**多个配置文件**。

![multiple phpunit configurations](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/test-multiple-configs.png)

另外，我们已修复：

- 在配置文件内执行所有测试。
- 在单个测试套件内执行所有测试。
- 正确的 Xdebug 指令，以免在调试测试时引发不必要的警告。

### ParaTest

此更新允许以与 PHPUnit 测试相同的方式运行 [ParaTest](https://github.com/paratestphp/paratest)。为此，请执行以下步骤：

- 使用命令 `Composer: require dev package` 安装 ParaTest composer 包，并搜索包 `brianium/paratest`。
- 更新您的工作区设置：
  ```json
  {
    "phpunit.phpunit": "./vendor/bin/paratest"
  }
  ```
- 导航至_测试_面板并运行或调试您的测试。

### 保存时排序使用

以下设置适用于保存时对 `use` 语句进行排序和组织：

```json
{
  "editor.codeActionsOnSave": { "source.organizeImports": true },
}
```

### 智能感应

现在可以通过 `Ctrl`+`点击`（或使用 `F12` 跳转）在 `@inheritdoc` 上直接导航到基础文档注释。[#897](https://community.devsense.com/d/897-jump-to-phpdoc-via-clicking-on-inheritdoc)

此外，签名帮助中的返回类型提示会遵循模板（泛型）参数。

### Composer `"composer.workingPath"` 设置

感谢反馈 [#909](https://community.devsense.com/d/909-setup-a-working-directory-for-composer)，我们新增了 `"composer.workingPath"` 设置，用户可以在其中指定 `composer.json` 和 `vendor` 文件夹的相对路径。

### 修复

- 修复了更新/移除工作区中的 `.phar` 文件时发生的内存泄漏问题。（通常发生在 `composer update` 和 `require` 时。）[#291](https://github.com/DEVSENSE/phptools-docs/issues/291)
- 自动补全后未自动添加括号 `()` 于 `array`，`require`/`include`，`exit` 和 `die`。
- 如果多行 HTML 属性用单引号包围并位于 PHP 块内，则在每次格式化期间会缩进。[882](https://community.devsense.com/d/882-one-more-auto-format-creeper) 
- 修复了在某些罕见情况下，混合 html/php 格式化导致格式化器停止的问题。[887-B](https://community.devsense.com/d/887-cannot-format-code-with-syntax-errors)

## 1.32.12895 (2023年3月28日)




### 智能感知

- 指定为 Doc Comment `@param` 类型的 `null` 被报告为无效。
- `true` 伪类型在联合类型中正确处理。
- 名为 `new()` 的方法在鼠标悬停和代码补全中正确处理。
- 对 Laravel 服务的检测得到改进。
- 实现了 `expectedArguments()` PHPStorm 元数据的初步支持。
- 在 `<?php` 标签后补全 `declare` 和 `declare(strict_types=1);`。

### 重构

- PHPDoc `@see` 和 `@uses` 在重命名重构、查找所有引用和高亮显示时被识别。
- 即使关闭 **problems** 设置，未使用的 `use` 检查也可正常工作。
- **命名空间导入** 对于任何简单类名。我们提供代码操作建议，以导入命名空间或完全限定类名，如果有多个具有相同名称的类。

#### 组织导入

我们已添加对 VS Code **"organize imports"** 命令的支持，以及最终的 `"editor.codeActionsOnSave"` 设置，允许您在自动保存文档时 _组织导入_ （即**去除未使用的 uses**）。

![organize uses](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/source.organizeimports.png)

### 修复

- 稳定性修复。
- 智能选择修复。
- 文件开头的 `#!` 不会报告为语法错误。
- 某些 `mixed` 类型上的属性不会报告为未知。
- 格式支持为分布在多行的 PHP8 属性缩进 [#879](https://community.devsense.com/d/879-php-8-attribute-code-formatting)
- 当 `readonly` 或 `static` 被用作函数参数名称时，格式不会移除空格。
- 修复了格式化器在 `new` 和 `()` 之间添加额外空格的问题 [#883](https://community.devsense.com/d/883-formatting-new-function-issue)

## 1.31.12821 (March 20, 2023)





### 修复

- 修复了路径导航。（[#302](https://github.com/DEVSENSE/phptools-docs/issues/302)）
- 未识别的 Psalm 和 PHPStan 特殊类型名称。（[#860](https://community.devsense.com/d/860-breadcrumb-bar-strange-behavior)）
- 全局变量类型检查修复 （[#303](https://github.com/DEVSENSE/phptools-docs/issues/303)）
- 鼠标悬停查看 `@mixin` 的属性。
- IntelliSense：Laravel 门面和 DocComment `@method` 的方法均能正确解析。
- 修复 VS Code 生成的 `rg` 进程问题。（[#877](https://community.devsense.com/d/877)）
- 修复复杂的 html/php 混合格式化问题。[#852](https://community.devsense.com/d/852-another-auto-format-error)
- 修复多行链式调用的缩进错误。[#862](https://community.devsense.com/d/862-formatting-bug)
- 修复在 `PSR-12` 中提供多行头时，方法或函数声明的开括号位置。[#305](https://github.com/DEVSENSE/phptools-docs/issues/305)
- 修复将 lambda 函数作为参数传递给方法或函数后出现的不必要的换行。[#306](https://github.com/DEVSENSE/phptools-docs/issues/306)
- 修复了实现接口的具有基础类型的枚举的格式。
- 修复函数调用为多行时命名参数的缩进。[#863](https://community.devsense.com/d/863-php-named-parameters-do-not-get-formatted-correctly)
- 在某些情况下以 html/php 混合格式调用时，选择的格式不起作用。
- 格式不会缩进 html 注释中的 php 代码块 [#872-3](https://community.devsense.com/d/872-syntax-highlighting-and-another-auto-format-creeper)

## 1.31.12740 (2023年3月4日)





### 内联提示

全新的 PHP 代码的**内联提示**上线啦！

![inlay hints](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-inlay-hints.png)

可用的内联提示包括参数名称、按引用传递的参数和推断的函数返回类型。

![inlay hints](https://docs.devsense.com/vscode/imgs/vsc-inlay-parameter-byref.png)

要启用或禁用内联提示，请更改以下**设置**：

- `"editor.inlayHints.enabled"`
- `"php.inlayHints.parameters.enabled"`
- `"php.inlayHints.parameters.byReference"`
- `"php.inlayHints.types.return"`
- `"php.inlayHints.types.variable"`

查看更多详细信息，请参阅[文档](https://docs.devsense.com/vscode/editor/inlay-hints)。

### 缺少文档注释的快速修复

新的代码操作添加了缺少的文档注释，包含推断的类型信息和摘要占位符。功能与在函数/类/属性/常量或 `define()` 调用上方键入 `/**` 相同，但可以通过代码操作调用，并且可以一次性在多个声明的整个选定代码上调用。([#226](https://github.com/DEVSENSE/phptools-docs/issues/226))

### 智能选择

Visual Studio Code 的选择范围功能允许快速选择语法元素；PHP 插件为所有语句、声明和代码块提供选择范围功能。

### 格式化

我们经常收到的另一个功能请求是引入 `Drupal` 代码风格 [#795](https://community.devsense.com/d/795-add-drupal-code-style-to-list)。所以我们很高兴地宣布 `Drupal` 代码风格已在此版本中引入。

格式化器现在支持 `files.InsertFinalNewLine` 选项。[#837](https://community.devsense.com/d/837-formatter-removes-a-new-line-after-a-class-closing-brace)

### 修复

- 修复了在定义预览时的高亮显示范围 ([#288](https://github.com/DEVSENSE/phptools-docs/issues/288))
- 修复了一些内部异常。
- 修复了当代码语法无效时鼠标悬停的问题。
- 修复了 "Search TODO" 命令在存在 remote:// 或 git:// 文件时的工作区问题，可能在使用 git 合并或差异窗口之后。
- 修复了 `.git` 和其他特殊目录中变动后的索引问题。
- Doc Comments 中指定的类型可以是 `$this` 作为 `self` 的别名，例如 `callable($this)` ([#843](https://community.devsense.com/d/843-error-in-parameter-type-with-docblock))。

### 格式化修复

- 修复了在对象在括号内时多个方法调用链接的格式化问题。[#820/8].(https://community.devsense.com/d/820-heredoc-with-interpolated-variables-breaks-auto-formatting-for-the-entire-file/8)
- 修复了混合 JS 和 PHP 的格式化问题。[#820/5](https://community.devsense.com/d/820-heredoc-with-interpolated-variables-breaks-auto-formatting-for-the-entire-file/5)
- 修复了 JS 格式化与内部 PHP 代码一起使用时每次格式化都会移动 `}` 的问题。[#820/7](https://community.devsense.com/d/820-heredoc-with-interpolated-variables-breaks-auto-formatting-for-the-entire-file/7)
- 修复了多行 HTML 属性、注释或 CDATA 的内容在每次格式化时缩进的问题。[#820/12](https://community.devsense.com/d/820-heredoc-with-interpolated-variables-breaks-auto-formatting-for-the-entire-file/12)
- 修复了当 Linux 行结尾在 PHP 文件中存在混合语言时导致不同格式输出的问题。
- 修复了 `use` 声明与类同名别名的问题，导致格式化器停止工作。
- 修复了当数组访问和成员使用在多行表达式中组合时的双重缩进。[#842](https://community.devsense.com/d/842-formatter-adds-unnecessary-tabs)
- 修复了在引用赋值中 & 符号后的不必要空格 [#846](https://community.devsense.com/d/846-spaces-after-symbol-ampersand-to-define-reference)，但同时也尊重 `$a =& $b;` 的这种表示法。
- 修复了多行表达式包含数组项访问时的不必要双重缩进。
- 修复了当行注释在 `elseif`、`catch`、`finally` 前出现时的不必要换行问题。
- 修复了在创建对象的新实例时 `static` 或 `self` 与 `(` 间的不必要空格。
- 修复了格式化器移除位运算符 & 周围空格的问题。
- 修复了分多行构造函数调用时对象字段访问的双重缩进问题。
- 修复了 `php.format.rules.alignConsecutiveAssignments` 与不同类型左表达式组合时的问题。
- 修复了当保留类型用作类型提示时缺少空格的问题。
- 修复了在多行链接函数调用中注释缩进错误的问题。
- 修复了 `)` 后偶尔缺少空格的问题，当使用 `php.format.rules.keepControlStatementsInOneLine` 选项时。[#852-2](https://community.devsense.com/d/852-another-auto-format-error/2)
- 修复了多行三元运算符中的不必要空格。
- 修复了与 PHP 关键字同名的函数后的不必要空格问题。
- 修复了使用 `static` 关键字时静态成员访问的双重缩进问题。
- 修复了在多行构造函数调用中访问成员时的缩进错误。
- 修复了在 `default` 命名的标识符后的不必要空格。
- 修复了在函数声明参数中使用的属性停止格式化器的问题。
- 修复了当命名空间中使用 trait 的 use 停止格式化器的问题。
- 修复了当 trait 使用更改可见性为 public 时停止格式化器的问题。

## 1.30.12484 (2023年2月10日)





### 修复

- 代码格式化修复。
- 修复各种缺失的标准函数和缺失的歧义。
- 在macOS上识别Homebrew `php`。
- 修复了带插值变量的heredoc格式化问题 [#820](https://community.devsense.com/d/820-heredoc-with-interpolated-variables-breaks-auto-formatting-for-the-entire-file)

## 1.30.12450 (2023年2月9日)





### 编辑器

**折叠 `use`** 已添加；这允许折叠 `use` 语句块（[tweet](https://twitter.com/JoelPiccoli/status/1622633203818176512)）。

### Getter/Setter

新增功能，通过设置 `"php.completion.getterSnippet"` 和 `"php.completion.setterSnippet"` 来自定义添加getter和setter时插入的代码。通过这种方式，您可以添加各种值处理并自定义返回值，或为自己添加注释（[#813](https://community.devsense.com/d/813-setter-without-self-reference)），例如：

```json
"php.completion.setterSnippet": "{PROPERTY} = sanitize(${NAME}) ?? throw new InvalidArgumentException('Invalid ${NAME}!');\n//done\nreturn {THIS};",
```

### 格式化

 - 支持有底值的枚举。
 - 新增设置 `php.format.rules.keepControlStatementsInOneLine`。[#810](https://community.devsense.com/d/810-is-there-an-option-to-not-auto-indent-one-liners)
 - 设置 `php.format.rules.SpaceBeforeColonInControlflowStatements` 重命名为 `php.format.rules.SpaceBeforeColonInControlStatements`。
 - 修复了类型声明中的不需要的空格 [#271](https://github.com/DEVSENSE/phptools-docs/issues/271)。
 - `php.format.rules.alignConsecutiveAssignments` 现在仅在赋值直接相邻时进行对齐。在赋值之间插入新行将迫使它们以不同方式对齐。

 ### 修复

 - 在差异视图中打开的文档不会在符号搜索和符号导航中出现两次（[#549](https://community.devsense.com/d/549-intellisense-remembers-old-method-parameters/11)）。
 - 修复了Unix上的符号链接递归（[#269](https://github.com/DEVSENSE/phptools-docs/issues/269)）。
 - 修复了空白的“更新内容”屏幕。

## 1.30.12417 (2023年2月7日)




### 文档注释

支持在文档注释中使用字面量和常量（例如在 `key-of<>` 和 `value-of<>` 中），因此文档注释中的类型信息可以被解析，并且 IntelliSense 在其中工作正常（[#801](https://community.devsense.com/d/801-key-of-and-value-of-support)）。

### 诊断

- 报告重复的提升属性。
- 报告修改只读属性。
- 如果存在 `__get`/`__set` 但也有 `@property` 文档注释声明，则报告使用未定义属性。
- 添加了未知属性类的诊断。

### 重命名重构

重命名 `class`、`interface`、`trait` 或 `enum` 时，建议同步重命名对应的文件（如果适用）。

### 悬停工具提示

新增了两个设置来配置悬停工具提示。

- `"php.hover.fullname"` 在工具提示顶部添加完整的类成员名称（包括类的完全限定名）（默认禁用）（[#808](https://community.devsense.com/d/808-show-class-name-in-function-description-on-hover-popup)）。
- `"php.hover.containingClass"` 允许启用/禁用显示类名作为函数工具提示的一部分（默认启用）。

### 修复

- 已优化整个工作区处理时间（源代码解析）。
- 添加了缺失的 `ZipArchive::` 常量（[#256](https://github.com/DEVSENSE/phptools-docs/issues/256)）。
- 显示在 IntelliSense 和代码诊断中的 lambda 函数内部定义的常量（[#257](https://github.com/DEVSENSE/phptools-docs/issues/257)）。
- 重命名构造函数提升属性的重构和语义高亮。
- `extends`/`implements` 关键字之后的上下文感知完成。
- 修复在工作区中存在许多 `.gitignore` 文件的情况下的 `"Problems: Exclude Git Ignore"`。
- 修复在函数声明上方定义的 `@global` 类型的使用。
- 修复在尾随逗号上方的 `/**` 生成文档注释（[#265](https://github.com/DEVSENSE/phptools-docs/issues/265)）。
- 修复当使用 `includePath` 与工作区路径重叠时的问题和代码分析更新。

## 1.29.12304 (2023年1月29日)




### IntelliSense 改进

**尊重 `@internal` 注解**

现在，使用 `@internal` 文档注释标记的符号在自动完成列表中会隐藏；

**正确排序**

我们更新了自动完成的排序方式，以根据上下文和已输入的文本进行排序；首先列出导入命名空间中的符号，然后是顶级符号，最后是可以自动导入的符号。

**弃用类**

此外，弃用的类和接口在代码完成列表中以及在源代码中使用时都会被删除线标记出来。之前我们只是针对函数这样做。

![deprecated classes and interfaces](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vscode-deprecated-types.png)

**性能**

更频繁的操作已移动到后台线程，以确保用户体验的流畅和不中断。

### 短开放标签 `<?`

我们已默认启用解析短开放标签 (`<?`) 内的 PHP 代码。这处理了 `<?xml` 在源代码开头的情况；

可以使用设置 `"php.workspace.shortOpenTag"` 禁用短开放标签内的解析。

### Composer

本地开发版本的 `composer.phar` 每30天自动更新一次。

### 修复

- 在 IntelliSense 中添加了缺少的 `pcntl` 常量。
- 修复了 `#region`/`#endregion` 折叠。
- 修复了在各种情况下的折叠。
- 修复了 `composer update` 后 IntelliSense 更新。
- 修正了工具提示中显示不正确的 `integer` 类型名称。
- 修正了全局变量重命名 ([#242](https://github.com/DEVSENSE/phptools-docs/issues/242))
- 修复了非en本地化中的警告信息 ([#249](https://github.com/DEVSENSE/phptools-docs/issues/249))。
- 修复了 `switch` 语句中缺少的不可达代码警告。
- 修复了在 `throw new` 之后代码完成中缺少的 `Exception` 类。
- 修复了有语法错误时的自动导入 ([#671](https://community.devsense.com/d/671))。
- 格式化器不会删除 `yield from` 后的空格 ([#248](https://github.com/DEVSENSE/phptools-docs/issues/248))。
- 带有前导 `/` 的 `use` 语句阻止了格式化器。
- 以 `;` 结尾并用空格与冒号块封闭标记分隔的冒号块阻止了格式化器。

## 1.28.12200 (2023年1月21日)





### 新代码操作

更多有用的重构即将加入PHP扩展和VS Code。以下是引入通用PHP 8语法到代码中的重构。

**条件 `?:` 可以替换为 `?->`**

简化以下类似的条件表达式：

![简化条件表达式](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-code-action-conditional.gif)

**可以简化赋值**

简化赋值：

![简化赋值表达式](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-code-action-assignment.gif)

**将 `switch` 转换为 `match`**

在某些情况下，`switch` 语句可以转换为新的 `match` 表达式。

### PHPStan条件返回类型

此更新增加了对新的PHPStan的条件返回类型的支持。这种方式指定的返回类型现在可以被正确识别，并在源代码中相应地上色，IntelliSense也会相应地使用指定的类型。

![phpstan 条件返回类型](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/phpdoc-phpstan-confitional-return.png)

### 改进的类型检查和IntelliSense

**重大变更：** 默认情况下，我们现在仅报告 _已打开文档内的_ 诊断。这可以通过设置 `"php.problems.scope"` 来更改。例外的是语法错误 - 那些会从整个工作区报告。

此外，修复了多种 _虚假_ 警告，主要是与泛型类型结合时的情况。整体上的类型分析得到了改进。

此外，大多数填充器不会干扰代码补全和符号导航；由于内建手册带有泛型类型参数注解，它优先于来自第三方包的填充器（[#241](https://github.com/DEVSENSE/phptools-docs/issues/241)）。

### 改进的补全排序

代码补全本身得到了改进，因此 _本地_ 符号应该优先列出。我们仍在努力改进这个功能，尽可能地优化。

### 修复

- 我们修复了内存泄漏和语言服务器崩溃的问题。
- 修复了输入 `/**` 后PHPDoc片段文本被损坏的问题。
- 添加了缺失的Psalm标量类型注释。
- 修正了解析 `@mixin` 成员的正确顺序（[#777](https://community.devsense.com/d/777)）。
- 可以将 `html` 文件与 `php` 语言支持关联。
- `//region`/`//endregion` 折叠（[#788](https://community.devsense.com/d/788-region-comments-won-t-fold)）。

### 格式化

- 删除可空返回类型中 `?` 符号后的不必要空格 [#752](https://community.devsense.com/d/752-extra-space-after-optional-type)
- **Wordpress** 代码风格的修复
  - 类型和函数声明不将 `{` 放在新行上
  - `Unset` 调用在括号内未格式化以带空格。
  - `exit()` 或 `die()` 在括号内不带空格。
- 在某些情况下，`php.format.rules.alignConsecutiveAssignments` 会导致格式化器停止工作。
- 使用不等于操作符 `<>` 而不是 `!=` 会导致格式化器停止工作。
- 构造函数头中的可选逗号在属性提升时导致格式化器停止工作。
- 在合并HTML和PHP时的某些情况下会导致格式化器停止工作。
- 当 `switch` 中的 `case` 后跟 `;` 而不是 `:` 时，格式化器会停止工作。

## 1.27.12010 (2023年1月9日)





### 文档注释语法

我们一直在努力识别文档块中的各种常用类型语法；现在支持大多数PHPStan和其他流行的静态分析工具。

此版本为文档块以及相关类型分析和代码诊断引入了更多的兼容性和功能。

### 着色和语义标记

PHP文档注释变得非常复杂，而像PHPStan这样的框架增加了更多语法和复杂性。我们支持大多数扩展语法，包括泛型类型、模板、类型别名、联合、交集、`callable`语法，以及数组形状；在此版本中，这些类型在_文档注释_中被相应着色。

![php callable 规范](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/callable-type-def.png)

整个类型表达式现在已被解析、着色和识别。工具提示显示了显示`Closure`参数和返回类型的签名帮助。

_注意：_ 更美观的工具提示正在进行中！

### PHPStan数组形状、`callable`、`list`及更多

从此版本开始，编辑器支持数组形状和可调用语法。此外，类型分析也相应地处理指定的PHPStan类型。

PHP Doc Comments中指定的PHPStan和Psalm **数组形状**是被允许的，可以解析、着色，并用于代码补全和类型分析。

此外，还处理了`list`和`non-empty-list`类型。包括使用`<`和`>`指定的泛型对应类型。

现在还支持PHP Doc Comments中的所有**可调用**语法。

### 更多通用注释

此次更新带来了使用泛型模板类型注释的标准类型；这在Laravel和Symfony框架中特别有用，因为它为所有集合、可迭代对象、`Generator`、`DOMNodeList`等提供了类型推断。

这改善了各种可迭代对象中`foreach`中的值推断。

### 变量的文档注释片段

在变量赋值之上或全局变量之上创建文档块时，现在可以配置将创建的片段。此外，片段设置有一个新属性`"singleline": true|false`（对于变量，默认是`true`），允许指定是否创建单行的文档块（即`/** @var Type */`）。

示例设置：

```json
{
    "php.docblock.variableSnippet": {
        "singleline": false
    }
}
```

### 修复

- `integer`、`boolean`、`list`类型在文档块中得到了正确处理。
- 修复了未使用的`use`分析，因此可以处理文档块中指定的类型名称。
- `session_set_cookie_params()`的诊断和参数补全在两种可能的定义中均有效。
- 添加了缺失的`Imagick`常量。
- 改进了对泛型类型和各种边界情况的类型推断。

## 1.26.11866 (2023年1月3日)





### IntelliSense 和枚举

PHP 8.1 的 `enum` 对象隐式实现了 `UnitEnum` 和 `BackedEnum` 接口。`BackedEnum<TValue>` 接口用模板类型参数进行了注解，以便在 Doc Comments 中与后备类型一起使用，以便更好的类型分析。例如：

```php
/** @param \BackedEnum<string> $e */
function foo($e) {
    return $e->value // -> string
}

enum MyEnum : string {
    case A;
}

foo( MyEnum::A );
```

**泛型和 Doc Comments 类型注解**

PHP Doc Comments 中的类型注解已重新实现，因此即使是复杂的结构也可以被处理、自动完成、重构、高亮和预览。高亮显示也适用于嵌套的泛型类型，以及重命名重构和代码自动完成。

```php
/**
 * @template TElement of \BackedEnum<string>
 * @return (Collection<int, TElement>|array<int, TElement>)[] 复杂泛型类型注解 */
```

**多行结构化数组类型**

此版本增加了对多行结构化数组类型注解的支持。这允许用户指定数组类型及其键和相应条目的类型。请参见下面的示例：

```php
/**
 * @return array
 *         {
 *           name: string,
 *           age: int,
 *         }
 */
```

### 代码诊断改进

我们一直在努力改进代码分析和相关诊断。本次发布避免了许多错误警告。

### 格式化

我们很高兴地推出新的 **Laravel** 代码风格。只需将 `php.format.codestyle` 设置为 `laravel`。 

现在您还可以通过选项 `php.format.rules.alignConsecutiveAssignments` 让格式化器自动对齐连续的赋值 [#692](https://community.devsense.com/d/692-sug-formatting-add-auto-align-option)。

```php
$a     = 1;
$bbb   = 2;
$ccccc = 3;
```

我们还增加了其他的格式化规则：

|Setting|描述|
|-------|----|
|`php.format.rules.spaceBeforeColonInControflowStatements`|在控制流块中的冒号前插入一个空格。|
|`php.format.rules.spaceBeforeColonInReturnType`|在返回类型中的冒号前插入一个空格。|
|`php.format.rules.spaceWithinCallParens`|在方法、函数和构造函数调用的括号内插入一个空格。|
|`php.format.rules.spaceWithinDeclParens`|在方法、函数和构造函数声明的括号内插入一个空格。|
|`php.format.rules.spaceWithinArrayInitilizersParens`|在数组初始化的括号内插入一个空格。|
|`php.format.rules.spaceWithinIfParens`|在 `if` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinWhileParens`|在 `while` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinForParens`|在 `for` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinForeachParens`|在 `foreach` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinSwitchParens`|在 `switch` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinCatchParens`|在 `catch` 语句头的括号内插入一个空格。|
|`php.format.rules.spaceWithinBrackets`|在方括号内插入一个空格。|
|`php.format.rules.spaceWithinBracketsAroundExpression`|在表达式周围的方括号内插入一个空格。|
|`php.format.rules.spaceWithinExpressionParens`|在表达式周围的括号内插入一个空格。|

我们还修复了一些格式化问题：
- 命名空间中的 `readonly` 会导致格式化器停止格式化
- 函数声明中的 `readonly` 和 `enum` 不会在括号前添加空格
- 现在支持 PHP 8.2 解构正常形式类型
- 在多行表达式中，常量使用时会被双重缩进 [#748](https://community.devsense.com/d/748-constant-arrays-are-being-double-indented)
- 我们解决了一些在混合 HTML 和 PHP 代码时导致代码看起来不整洁的情况。最明显的是在 **Wordpress** 模板中。

### 修复

内置 PHP 函数类型分析的紧急修复。

## 1.26.11753 (2022年12月28日)




### 类型分析改进

- 现在使用 `assert()` 语言结构中的表达式来确定变量类型。([#744](https://community.devsense.com/d/744-support-assert-to-determine-type))
- 某些类型注解现在更加精确。
- 箭头函数内的隐式闭包变量现在已正确初始化。这修复了关于在嵌套箭头函数内使用未初始化变量的错误警告。
- 更多核心类型已使用模板类型参数进行注解，允许在使用 `@template` 和类似方法的地方更好地推断类型 ([#746](https://community.devsense.com/d/746))。
- 改善了对泛型的支持，以正确处理 doctrine/collections 和其他使用扩展 `@template` 语法的模板类型 ([#746](https://community.devsense.com/d/746))。

### 编辑器改进

- 当 `readonly` 和 `enum` 关键字作为命名空间或函数声明的一部分使用时，不再错误地报告为语法错误。
- 在代码补全过程中，语言服务器的内存分配显著减少；这提高了整体性能。

### 格式化

- 在 **Wordpress** 代码风格中，我们不再在空括号和方括号之间插入空格，例如 `foo()`，但 `foo( 1, 2 )`。
- 不对齐数组初始化中的键值对，当它们不在单独的一行时（当 `php.format.rules.arrayInitializersAlignKeyValuePairs` 启用时）。
- 修复了多行表达式中常量的错误缩进问题。

### Apple Silicon

引入对 Apple **M1** 和 **M2** 芯片（**Apple Silicon**）的支持。这些 `arm64-x64` 架构的 CPU 在之前的版本中未被完全支持，我们很高兴现在为这些架构提供语言服务器。

## 1.25.11652 (2022年12月21日)





### PHP 8.2

内置的IntelliSense已更新，以在所有可用语言中提供最新的PHP 8.2类、函数、常量和文档（[#215](https://github.com/DEVSENSE/phptools-docs/issues/215)）。

作为PHP 8.2的一部分，我们添加了新的 `Random` 扩展的多语言文档集成。

### 格式化

我们经常收到的反馈之一是，有时格式化速度较慢。我们已解决这些情况，现在应该好很多了。但是，如果遇到不快的情况，请告知我们。

我们还很高兴地介绍**Wordpress**代码风格。只需将 `php.format.codestyle` 设置为 `wordpress` 即可。尽管我们仍需实现一些规则，但它已基本就绪。

在此版本中，我们还关注了混合html/css/js/php的代码格式化。这很棘手，因为html代码的缩进会影响php代码，反之亦然 [#171](https://github.com/DEVSENSE/phptools-docs/issues/171)。我们认为现在处理得很好，希望**wordpress模板**在格式化后看起来不错。

### 修复

- 在VSCode首次启动后直接的第一次格式化请求中，仅php代码被格式化。
- 无论html匹配标签内是否有php标签，均应高亮显示。[#172](https://github.com/DEVSENSE/phptools-docs/issues/172)
- 带有尾随逗号的函数参数列表的换行，停止了格式化器。
- 以命名空间反斜杠为前缀的函数调用缩进不正确。
- 在javascript中插入不需要的php代码空格。[#222](https://github.com/DEVSENSE/phptools-docs/issues/222)
- 格式化时，php代码的缩进可能由开放标签的位置决定不正确。格式化器需要第二次通过才能正确。
- 代码诊断修复：
  - 某些情况下未报告 `parent::` 作为静态调用。
  - 嵌套箭头函数中的局部变量未报告为未初始化。
  - 从基类继承 `@param` 类型，如果没有文档注释。
  - 移除旧 `@param` 语法的支持 [#740](https://community.devsense.com/d/740)。
  - 修复嵌套二元表达式的控制流分析。
  - 添加对替代文档注释数组语法的支持，例如 `(int|string)[]`。
  - 修复更复杂泛型类型继承的类型分析。
  - 添加对泛型 `IteratorAggregate<TValue>` 的支持。
  - 泛型类型在工具提示中正确传播和替换。

## 1.25.11537 (2022年12月11日)





### 悬停工具提示改进

新增功能：鼠标悬停工具提示显示**参数说明**。可以使用设置 `"php.hover.parameters"` 来更改此行为。

可以通过新的设置 `"php.hover.documentation"` 启用或禁用鼠标悬停工具提示中的文档链接。

### 泛型

模板类型推断和替换已得到改善，以处理更复杂的类型层次结构。 ([#723](https://community.devsense.com/d/723), [#733](https://community.devsense.com/d/733), [#731](https://community.devsense.com/d/731))

### 修复

- 生成的**文档注释**遵循 `yield` 并正确为函数添加 `Generator` 类型提示。另外，代码诊断遵循返回 `Generator` 的函数并正确分析返回值类型。

- `'enum'` 关键词是 PHP 本身的一点技巧。我们已修复其解析方式，使其正确适用于 PHP 5, 7, 8 和 8.1 及以后的版本 ([#205](https://github.com/DEVSENSE/phptools-docs/issues/205))。

- 在生成自动函数覆盖时，括号 `()` 的自动补全只插入一次 ([#730](https://community.devsense.com/d/730))

- 修复了_转到定义_功能。

### 格式化

#### 新的自定义设置

如承诺的那样，我们根据您的反馈添加了更多格式化选项。

|设置|描述|
|-------|-----------|
|`php.format.rules.spaceBeforeParenthesesInArrowFunctions`|箭头函数中括号前的空格|
|`php.format.rules.spaceAroundConcatenation`|连接符 `.` 周围的空格|
|`php.format.rules.spaceAfterUnaryNot`|一元取反 `!` 后的空格|
|`php.format.rules.groupUseWrap`| 定义分组使用的换行行为 |
|`php.format.rules.groupUseNewLineBeforeFirstDeclaration`|在第一个分组使用声明之前放置新行|

#### `foreach`

我们现在默认将 `foreach` 语句头压缩为一行（如 `PSR-12` 中定义）。

```php
<?php 
foreach ($iterable as $key => $value) {
}
```

#### `PSR-12`

我们稍微改进了 `PSR-12` 代码样式。现在，我们将自动根据标准包裹多行分组使用声明。

```php
<?php
use Vendor\Package\SomeNamespace\{
    SubnamespaceOne\ClassA,
    SubnamespaceOne\ClassB,
    SubnamespaceTwo\ClassY,
    ClassZ,
};
```

#### 修复

- 当匿名类实现列表定义在多行上时，我们未正确缩进它们
- 实现列表换行设置也适用于匿名类

## 1.24.11420 (2022年12月1日)





### 数组形状

编辑器现在处理在文档注释中指定的内联数组形状。以下语法是正确的，并且被PHP编辑器理解：

```php
<?php

/**
 * @param array{ name: string, id: int, data: \App\Model\User } $a 实体。
 */
function foo($a) { .. }
```

数组形状提高了代码补全功能，因为它为数组键提供了代码补全；并推断类型，因为它根据指定的索引解析数组项的类型。

### IntelliSense 改进

**括号补全**

IntelliSense现在能够在补全函数时补全括号。光标置于括号之间。此功能可以选择禁用，也可以将完整的函数签名作为代码片段完成。这样可以使用 `[tab]` 键在参数之间跳转并填写参数。

该功能可通过设置 `"php.completion.parameters"` 配置。默认情况下，它被设置为 `"parentheses"`，因此只补全括号 `()`。

![php complete parentheses](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-complete-parentheses.gif)

**Xdebug 存根**

我们为 **Xdebug** 扩展添加了存根。前往设置，并将 `"xdebug"` 添加到 `"php.stubs"` 设置中：

```json
{ "php.stubs": ["*", "xdebug"] }
```

这将 _Xdebug_ 功能添加到 IntelliSense、代码诊断，并改进类型推断分析。

**弃用消息**

每当使用弃用的符号时，它将被划掉并显示相应的警告。此外，在本次发布中，我们在代码补全提示中添加了弃用消息。

![php deprecation message](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-deprecated-message.png)

注意，要标记函数为弃用，请在下面类似地添加 `@deprecated` 文档注释标签：

```php
/** @deprecated 请勿使用此函数，自1.2.3版本起不再维护！ */
function getEntity(array $row) : object { ... }
```

### 可自定义格式化器

许多公司在编写源代码时都有编码指南，这可能与我们预定义的代码风格不同。我们很高兴地推出高度可自定义的格式化器，我们开始提供大约`30`种不同的代码格式选项。这只是开始，欢迎提供建议以便确定优先支持的选项。

这些更细化的代码格式选项仅对 `PREMIUM` 用户可用，但社区版用户仍然可以通过 `php.format.codestyle` 选项影响格式。

例如，您可以让格式化器通过 `php.format.rules.arrayInitializersAlignKeyValuePairs` 选项来自动对齐数组初始化中的键值对 [#692](https://community.devsense.com/d/692-sug-formatting-add-auto-align-option)。

```php
$x = [
    1    => 'foo',
    1234 => 'bar'
];
```

或者，如果您和您的公司偏爱 `Whitesmiths` 风格，您可以通过将 `php.format.codestyle` 设置为 `allman` 并将 `php.format.rules.indentBraces` 设置为 `true` 来进行设置 [#689](https://community.devsense.com/d/689-whitesmiths-style-sometimes-termed-wishart-style)。

```php
function foo()
    {
    echo "Hello";
    }
```

一般来说，使用 `php.format.rules.*` 设置来配置格式化器，使其行为如您所愿。有关详细的格式化选项列表，可以打开设置编辑器（`Ctrl+,`）并在搜索栏输入 `php format`，或者查看我们的[文档页面](https://docs.devsense.com/vscode/editor/customize-formatting)。

### 即时格式化

我们重新实现了即时格式化的行为。现在它能够正确识别您正在编辑的代码部分，并在输入 `;` 或 `}` 时对其进行格式化。这样，您的代码始终保持正确格式，而无需显式调用格式化命令。

我们建议开启此功能。在默认情况下，VS Code中是禁用的。

如果您希望仅针对 PHP 启用此功能，可以在 `settings.json` 中进行设置：

```json
"[php]": {
  "editor.formatOnType": true
}
```

### 格式化修复

- 拥有多个参数且在主体中包含 `func_get_args` 或 `func_num_args` 的函数停止格式化。
- 多行的使用trait语句会被双重缩进。
- 嵌套在特定语句头中的lambda函数缩进修复。
- 修复了当部分链是字段时，链式方法调用的缩进问题。 [#715](https://community.devsense.com/d/715-if-expression-without-braces-indents)
- 正确缩进了跨多行的静态方法调用的参数。
- 修复了多行字段的使用缩进，包括静态字段或常量。
- 支持安全空操作符。
- 支持属性。

### IntelliSense 修复

**控制流**

我们修复了控制流分析问题，当存在永不返回的函数时（即它们抛出异常而不是返回值）。相应地，修复了有关不可达代码的错误警告以及相应的变量类型推断。

**Lambda `use ()` 中的尾随逗号**

修复了 lambda 声明中不支持尾随逗号的问题（[#207](https://github.com/DEVSENSE/phptools-docs/issues/207)）。

**Blade**

我们修复了`.blade.php`文件中 `@can`、`@endcan`、`@forelse`和 `@empty`的使用问题。

**`"php.stubs"`**

修复了配置设置 `"php.stubs"`。在重新加载工作区后不再工作的问题。

## 1.23.11234 (2022年11月10日)





### `launch.json` 使用 `"envfile"` 选项

现在，你可以指定内置 PHP 服务器使用的 `.env` 文件。这对于开发 **Laravel** 应用程序尤其重要！示例启动配置如下所示：

```json
{
    "name": "Start Built-in Server with .env",
    "type": "php",
    "request": "launch",
    "runtimeArgs": ["-S", "localhost:8888", "-t", "public"],
    "envfile": ".env"
}
```

### 文档注释生成器

生成的 PHP 文档已得到改进。它在可能的情况下，在属性和类常量上指定 `@var`。另外，如果函数被识别为从不返回，它将返回类型注解为 `@return never` ([#193](https://github.com/DEVSENSE/phptools-docs/issues/193))。

### 快速修复

getter 和 setter 的快速修复现在遵循 `PSR-12`。此外，它以正确的形式指定了类型提示。

为生成 `__construct()` ([#198](https://github.com/DEVSENSE/phptools-docs/issues/198)) 的快速修复现在正确生成了文档注释。生成的函数也符合 PSR-12。

接口实现的快速修复也已更新，遵循 PSR-12 并正确生成类型名称。

### PHP 8.2

PHP 编辑器支持剩余的 PHP 8.2 特性。

- 新增，代码补全中包含了特殊属性 `#[SensitiveParameter]`。
- 此外，可以在常量表达式中使用 `enum` 案例值，如在 RFC 中规定的那样。

### 格式化

#### `PSR-12`

在此版本中，我们为 `PSR-12` 代码风格引入了更多规则。特别是它们指导格式化程序在格式化分为多行的控制语句头时如何表现。

例如：
```php
for ($i = 0; $i < 10; $i++
    ) {
    // for body
}
```

格式化为：

```php
for (
    $i = 0;
    $i < 10;
    $i++
) {
    // for body
}
```

以同样的方式，当 `implements` 列表分为多行时，我们将第一个项目放在下一行，并确保每个接口一行。

现在，当包装函数或方法调用时，我们还考虑使用了哪种类型的参数。当单个参数分为多行时，例如数组或 lambda 函数，我们不认为这是分割参数列表的理由。（此行为根据[PSR12 规范](https://www.php-fig.org/psr/psr-12/#47-method-and-function-calls)）

```php
<?php

somefunction($foo, $bar, [
  // ...
], $baz);

$app->get('/hello/{name}', function ($name) use ($app) {
    return 'Hello ' . $app->escape($name);
});
```

#### 格式化选择

我们改进了格式化选择的工作方式，这也会影响启用了 `editor.formatOnType` 和 `editor.formatOnPaste` 的情况。

#### 修复

同时，我们修复了 JavaScript 格式化程序在 PHP 代码中添加空格的问题 [#203](https://github.com/DEVSENSE/phptools-docs/issues/203) 和 HTML 格式化程序编辑 PHP 代码内容的问题。这主要表现在启用了 `editor.formatOnPaste` 选项时。

接下来，我们还解决了一些格式化问题：
  - 当语句为多行时，构造函数关闭 `)` 有时缩进不正确。
  - 某些情况下注释缩进不正确。
  - 单行方法调用不应换行。[#693](https://community.devsense.com/d/693-sug-formatting-don-t-wrap-when-there-is-no-data-in-brackets)
  - 在函数体中使用 `func_get_args` 或 `funct_num_args` 的函数会导致格式化程序停止。[#691](https://community.devsense.com/d/691-bug-formatting-not-working-when-there-are-specific-functions)
  - 只有以 `*` 开头的多行注释缩进 +1。
  - 有时在数组初始化器后面会不必要地添加新行。
  - 当包含元素换行时，lambda 不会换行。
  - 当构造函数存在于多行数组中时的双缩进修复。
  - 多个 lambda 的数组缩进错误。[#702](https://community.devsense.com/d/702-code-format-array-with-multiple-anonymous-functions)
  - 括号表达式没有缩进。[#700](https://community.devsense.com/d/700-code-format-if-condition-with-braces)
  - 多行使用 traits 声明现在正确缩进。
  - 某些情况下可选返回类型后的新行折叠。[#704](https://community.devsense.com/d/704-code-format-abstract-function)

## 1.22.11089 (2022年10月31日)





### PSR-12 格式化

我们很高兴地宣布引入 **PSR-12** 代码风格。在之前的版本中，我们已经涵盖了PSR-12兼容格式化程序所需的重要规则。我们仍会改进一些小问题，但基本上已经完成。同时，我们将默认的格式化代码风格从旧的PSR-2切换为PSR-12。

![PSR-12 code style](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/psr-12.png)

为了符合规范，我们还增加了以下规则：
 - 在 `catch (OtherThrowableType | AnotherThrowableType $e)` 的异常类型之间添加空格
 - 在函数声明头部压缩空格，使返回类型与 `)` 括号在同一行

符合 `PSR-12` 规范很重要，但代码在格式化后的外观同样重要。我们也在持续改进代码的美观性。本次发布中，我们处理了数组初始化的方式。如果数组中任何地方有新行，那我们会将所有数组项放在新的一行并进行缩进。[#683](https://community.devsense.com/d/683-code-format-array-new-line)。

![Array initializer](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/array_initializers.gif)

类似地，我们也对调用参数和函数/方法声明应用类似的行为，但仅限于 `PSR-12` 代码风格。

我们还修复了一些小的格式化问题。

### Composer 改进

`create-project` 命令已更新。如果不清楚您希望在哪里创建新项目，现在系统将打开打开文件夹对话框。最后，它会在 VS Code 中打开新创建的项目。

### 新的代码诊断

现在会报告接口内属性的无效声明。（[#174](https://github.com/DEVSENSE/phptools-docs/issues/174)）

此外，代码分析处理了默认的 **Laravel** 类别名。这影响到 IntelliSense 并避免错误的代码警告。

更多更新见下文的 **修复**。

### 修复

代码诊断对类型杂糅更宽松（即在 `for` 循环中的 `int` 到 `float` 类型杂糅），并且更好地推断数组元素类型。（[#185](https://github.com/DEVSENSE/phptools-docs/issues/185)）

此外，我们修复了使用 `func_get_args()` 处理可变数量参数的函数的代码诊断。（[#677](https://community.devsense.com/d/677-problem-with-func-get-args-and-phpdoc/5)）

还存在问题：在 composer 包移除或更新后，问题和 IntelliSense 没有及时更新——我们对此进行了更改，使一切如预期无缝更新。（[#182](https://github.com/DEVSENSE/phptools-docs/issues/182)）

## 1.21.10985 (October 23, 2022)





### 函数参数上方的 `@var`

编辑器处理紧挨着函数参数定义上方的文档块。如果有带类型说明的 `@var`，则会在 IntelliSense、工具提示和代码诊断中用于参数类型。

```php
class MyClass {
    function __construct(
        /** @var T[] */
        public readonly $list, // $list 是类型为 T[]
    ) { }
}
```

### 格式化

外观很重要。因此我们继续努力让它变得更美观：

 - 在访问属性或调用方法的多行表达式中，缩进级别增加了 [#530](https://community.devsense.com/d/530-formatting-keep-braces-in-the-same-line/18)
 - 在所有代码风格中，我们对 PHP 标签内的代码进行了缩进。 [#173](https://github.com/DEVSENSE/phptools-docs/issues/173)
 - 在某些情况下，当 HTML 与 PHP 结合时，会出现意外的新行 [#173](https://github.com/DEVSENSE/phptools-docs/issues/173#issuecomment-1280021048)
 - PHP 关闭标签 `?>` 根据之前的 `<?php` 开启标签进行缩进

### 改进

#### PHPUnit 测试视图

此更新改进了 _测试视图_ 面板中的 PHPUnit 测试解析。处理测试文件更加快捷，避免了冗余的磁盘读取和解析。此外，测试视图现在支持来自继承类的测试 ([#678](https://community.devsense.com/d/678-phpunit-test-explorer-ignores-tests-inside-abstract-parent-testcase-class))。

## 1.20.10937 (2022年10月19日)





### 编辑器改进

#### 高亮控制结构

新增了高亮控制结构和相应关键字的功能。编辑器现在可以高亮显示诸如 `for`、`foreach`、`while` 或 `do` 等控制结构，以及相应的 `continue` 或 `break`，当你将光标移动到它们上面时。同时，所有的 `return` 在函数中都被高亮显示，`case` 和 `default` 标签也是如此。

它还高亮显示匹配的 `switch`/`endswitch`、`if`/`elseif`/`endif`、`try`/`catch`/`finally` 等成对元素。

![highlight if/elseif/endif](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/highlight-control-structure.png)

#### 模糊搜索工作区中的符号

通过工作区搜索支持模糊查询；即符号名称与查询中的字母匹配。此外，使用大写字母搜索是区分大小写的，因此您可以快速搜索驼峰式表示法。

![fuzzy search symbols in worksspace](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/fuzzy-search.gif)

#### 格式化

我们正在通过更多情况来改进格式化支持。 

- 现在类型转换运算符会以空格分隔。 ([#175](https://github.com/DEVSENSE/phptools-docs/issues/175)).
- 构造函数属性提升被正确格式化。 [#176](https://github.com/DEVSENSE/phptools-docs/issues/176)
- 在某些情况下，在 `::class` 后被添加了不必要的空格。 [#530](https://community.devsense.com/d/530-formatting-keep-braces-in-the-same-line/26)
- 当 `else` 或 `elseif` 出现在语句之后时，它们会被放在新的一行。 [#530](https://community.devsense.com/d/530-formatting-keep-braces-in-the-same-line/25)
- 当类型引用与 `?` 分隔，如果它是三元运算符的一部分，会间隔一个空格。 [#530](https://community.devsense.com/d/530-formatting-keep-braces-in-the-same-line/19)

### 诊断改进

#### 新设置 `"php.problems.scope": "opened"`

现在您只能诊断在编辑器中打开的 PHP 文件。请注意，语法错误仍将在整个工作区中报告。

设置 `"php.problems.scope": "opened"` 来查看其工作效果。

#### 检查参数过多

现在我们检测 `func_get_args`、`func_get_arg` 或 `func_num_args` 的使用，这样就能检测到带有可变参数数量的函数，而不会报告 _too_many_args_ 警告。

## 1.19.10893 (2022年10月16日)





### 新格式化器

我们重新设计并更新了内置的PHP代码格式化器。通过设置 `"php.format.codeStyle"` 提供了几种新的格式化样式。

#### **`Allman`**

`Allman` 风格以 Eric Allman 命名。此风格将大括号放在下一行。适用于所有控制语句和声明。

```php
while ($x == $y)
{
    foo();
}
```

#### **`K&R`**

`K&R` 风格（Kernighan & Ritchie Style）在控制结构、类型、函数和方法上保持开放大括号在同一行。

```php
while ($x == $y) {
    foo();
}
```

您仍然可以继续使用先前支持的代码风格：

- `"PSR-2"` 风格，
- 类似于 Visual Studio 的风格称为 `"PHP Tools"`，
- 以及 `"Off"`，

该格式化器支持 HTML/JS/CSS，格式化范围、格式化整个文档，并且在输入时格式化 - 例如关闭代码块或语句后。

![Formatting multi-line expression](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/format-document.gif)

#### 格式化修复

以下是我们修复和实施的格式化问题列表：

- 箭头函数格式化修复。
- 格式化支持嵌套函数调用。
- 修复枚举的格式化问题。
- 修复与 `match` 表达式相关的格式化问题。
- *Heredoc* 和 *Nowdoc* 表达式在格式化期间保持不变。
- 格式化时正确缩进组合的 `use` 语句。
- 缩进多行控制语句头部。
- 在 lambda 中的多行表达式被缩进。
- 带有注释的空块被缩进。
- 组合 `use` 语句和 `match` 表达式尊重可选的尾随逗号。
- 在格式化函数参数时，类型与符号 `type &$x` 之间有空格。
- 缩进带有注释的空块。
- 匿名类型中的多行表达式被缩进。
- 多行函数和方法调用被正确缩进。
- 在函数或方法头部上的括号在新行上时不缩进。
- 修复 lambda 表达式后错误的新行。
- 格式化保留单行php块。
- 闭合标签始终与前一标记分开。
- 格式化函数的命名参数。
- 如果在与类头部同一行上，匿名类在 `{` 前有空格。
- 修复在 HTML 属性中的 PHP 代码格式化（例如 `<div style="<?php echo "something" ?>">`）。格式化器不再添加额外的空格。

### 突出显示待办注释

编辑器新增高亮显示代码中的待办事项注释。这有助于跟踪未完成的工作和待处理的问题。

![highlight todo](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/highlight-todo.png)

您可以使用以下设置自定义样式：

```json
"php.highlight-todo.style" : {
    "backgroundColor": "#ec0"
}
```

或者您可以通过设置 `"php.highlight-todo.enable": false` 完全关闭此功能。

### 调试器代码补全

在调试期间，当在 _Debug Console_ 中输入时，将建议现有的本地变量名称。输入 `$` 或补全快捷键（默认 `Ctrl`+`Space`），将建议可用的本地变量。

![debugger code completion](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-debug-completion.gif)

### 新诊断

编辑器检查并报告以下诊断：

- 静态调用实例方法。([#641](https://community.devsense.com/d/641-static-call-to-instance-method-not-detected))
- 对类型属性的无效赋值。([#647](https://community.devsense.com/d/647-assigning-wrong-types-is-not-detected))
- 提供给函数调用的参数过多。([#645](https://community.devsense.com/d/645-wrong-number-of-function-call-arguments-not-detected))
- 允许对象用于常量，并处理使用 `@var` 的 Doc Comment 上的 `const`。

### 新设置

我们添加了一个新设置 `"php.problems.excludeGitIgnore"` ([#169](https://github.com/DEVSENSE/phptools-docs/issues/169))，可让您忽略工作区`.gitignore`中指定的文件/文件夹中的代码诊断。

### 修复

- 生成 `__construct()` 的代码操作遵循文本编辑器的制表符和空格设置。
- 生成 Doc 注释 (`/**`) 符合缩进。
- 在函数上方生成 Doc 注释遵循自定义的 Doc 注释片段（`php.docblock.functionSnippet` 设置）。
- 修复了一些情况下，在添加 Composer 包后 IntelliSense 没有更新的问题。

## 1.18.10692 (2022年9月30日)




### 分析器支持 🔥

PHP代码分析允许您检查代码中每个函数被调用的次数以及消耗的时间。

[阅读更多 (docs.devsense.com) ...](https://docs.devsense.com/vscode/profiling)

**我们增加了对Xdebug分析的支持！** Xdebug分析文件（cachegrind格式）可以打开、查看和检查。根据分析结果，扩展还会在您的代码中突出显示热点路径。

**调用次数视图：**

![php call times view](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/profile-calltimes.png)

**调用者/被调用者视图**

详细查看调用者和被调用函数，包括调用时间。

![php callers callees](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/profile-details.png)

**热点路径装饰**

分析结果文件被分析，并直接在源代码中突出显示热点路径：

![profiling hot path decoration](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/profile-highlight.png)

### 更新的代码诊断

- 现在使用箭头函数内部的变量不会被报告为未初始化 ([#664](https://community.devsense.com/d/664-bug-when-use-use-keyword-inside-arrow-function-inside-anonymous-function))。
- 诊断 `PHP1408` 和 `PHP1409` 现在会报告为较低严重程度。

### Open-VSX

整个扩展现在在 [open-vsx.org](https://open-vsx.org/extension/devsense/phptools-vscode) 上可用

### 其他改进

- 自动导入的 'use' 已排序 ([#666](https://community.devsense.com/d/666-auto-import-alphabetically))。
- 修复了HTML代码格式化问题。
- 修复了构造函数属性提升格式问题。

## 1.17.10641 (2022年9月26日)





### 介绍 **What's New**

我们收到许多有用的功能请求和反馈，并且我们正在努力添加尽可能多的改进。其中之一就是简要地通知新功能。此次更新中，我们开始通过 **What's New** 窗口显示主要更新内容。

该窗口可以通过命令 `"PHP Tools: Release Notes"` 手动打开。当每次主要更新后自动打开可以在窗口底部通过复选框禁用。

  ![release notes command](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-open-releasenotes.png)

### 调试

调试具有一些不错的功能！更多设置用于启用性能分析，`var_dump()` 会产生更漂亮和更详细的消息，调试开始时确定 PHP 的 Xdebug。

#### 调试 `develop` 模式

从此次发布开始，我们已启用 `develop` Xdebug 模式。这会提供更好看和信息更丰富的 `var_dump()` 输出。

如果您更喜欢常规外观的 `var_dump()` 消息，请更改 `launch.json` 配置文件中的 `"noDevelop"` 设置。

#### 调试 `profile` 模式

您现在可以启用 `profile` 模式。在 `launch.json` 配置文件中设置 `"profile": true`：

```json
{
    "name": "Launch & Profile built-in Server",
    "type": "php",
    "request": "launch",
    "runtimeArgs": ["-S", "localhost:8000", "-t", "."],
    "noDebug": true, // <-- 不启动调试
    "profile": true // <-- 启用 xdebug.mode "profile"
}
```

#### 未捕获异常过滤器

在调试视图中新增了选项，可以选择中断或忽略**未捕获的异常**。此选项位于“调试和运行”视图中的“断点”面板中。

### 代码诊断

- 我们修复了在 `enum` 的 case 值情况下不正确的重复键检查。 ([#658](https://community.devsense.com/d/658-problem-with-enums-as-keys))
- 修复了当返回类型提示为 `void` 时的返回类型检查。
- 报告匿名函数中未使用的 `use` 变量。
- 报告匿名函数的 `use` 变量未初始化。
- 报告空命名空间。
- 检查从返回 `void` 类型的函数中返回的值是否被使用。
- 报告在 `void` 类型上访问属性。
- 检查字符串插值中的表达式是否可转换为 `string`。
- 检查属性的类型是否已定义。
- 如果用户只打开单个文件而未打开工作区或文件夹，则对未知类或未知函数的诊断将被抑制。
- 诊断 `0412` 的严重性已更改为*错误*，代码 `1412`（使用未分配的变量）。

### Composer

已添加了一体化的 **Composer** 集成！它实现了用于请求、移除和浏览包的有用命令，自动安装 `composer.phar` 以免您手动操作，为 `composer.json` 添加 IntelliSense，为运行脚本添加代码透镜，为已安装的软件包提供简洁的工具提示，检查已废弃的软件包等！

### 其他改进

对 PHP 格式化器进行了修复。当使用不太常见的数据类型别名进行显式转换（例如 `(integer)`、`(boolean)` 或 `(real)`）时，格式化未执行。

## 1.15.10535 (2022年9月14日)




### 命令 `PHP: Search todo ...`

引入了一种快速浏览PHP代码中所有待办注释的方法。命令 `"PHP: Search todo ..."` 打开快速选择器，显示所有待办事项。它允许筛选、搜索和导航到选定的项目。

  ![searching to-do in PHP code](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-search-todo.gif)

### 工具提示更好看了

如果函数签名的悬停提示过长，现在会拆分成多行。此外，可选参数不再用 `[` `]` 标注了。 ([#159](https://github.com/DEVSENSE/phptools-docs/issues/159))

  ![long function tool-tip](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-long-tooltip.png)

此外，代码注释中的安全HTML标签现在可以在工具提示中很好地呈现。像 `<br/>`, `<b>`, `<i>`, `<ul>`, `<li>`, `<code>` 这样的标签可以在文档注释中使用，并在工具提示中显示时呈现良好且格式化。

  ![html tool-tip](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/master/docs/vscode/imgs/vsc-html-tooltip.png)

### 代码诊断

我们添加了更多的诊断，并修复了代码流分析中一些罕见的情况。

- 对于无效使用 `break;` 的诊断，当 `break` 或 `continue` 超出允许范围时会提示。
- 修复了 `try`/`finally` 的代码可达性诊断。
- 在函数返回值中含有类型提示 `mixed` 但函数未返回值的情况下，提升了返回值诊断。

### 其他改进

修复了内部异常，并进行了多项性能和内存使用优化。

## 1.14.10471 (2022年9月7日)




- 新增 `"php"` **任务定义**；这允许定义在 VS Code 中执行 PHP 脚本的任务，并使用当前配置的 "php" 可执行文件：
  ```json
  // .vscode/tasks.json
  {
      "type": "php",
      "file": "${workspaceFolder}/script1.php",
      "args": ["argument"]
  }
  ```
- **设置** `"phpunit.preTask"` 和 `"phpunit.postTask"` 允许指定从 `tasks.json` 中执行的一个或多个任务，以便在测试运行之前或之后执行任务（[#154](https://github.com/DEVSENSE/phptools-docs/issues/154#issuecomment-1207248667)）。
  - 在 `phpunit.preTask` 和 `phpunit.postTask` 中执行的任务可以使用变量 `${command:phpunit.filter}` 或 `${command:phpunit.testsuite}`
- **设置**自定义通过输入 `/**` 生成的 DocComments（_PHPDoc_）
- **诊断**：
  - 报告重复的字段声明
  - 报告重复的类常量声明
  - 如果没有对应的 `__get`/`__set` 方法，或 `@property` 注解，报告动态属性
  - `foreach` 控制变量可以用 DocBlock 注释
- **智能感知**：更新了 PHP 8 `Attribute` 类声明及其成员
- **获取器/设置器**代码操作支持 `static` 属性

## 1.13.10390 (2022年8月30日)




- 修复了粘贴时的格式问题

## 1.13.10378 (2022年8月29日)




- 修复了HTML/CSS/JS编辑器功能
- 在PHP文件中启用HTML/CSS/JS格式化
- 修复了格式导致后续代码中断的问题（[#156](https://github.com/DEVSENSE/phptools-docs/issues/156)）

## 1.13.10301 (2022年8月16日)




- 支持 **PHP 8.2** 只读类。
- 一些 **PHP 8.2** 兼容性检查。
- _转到定义_ 命令可导航到 `include`/`require` 目标文件。
- 伪常量的工具提示显示正确的值。
- 在 `new`、`use`、`extends` 或 `implements` 后按下空格键可触发代码补全。
- 支持非标准文档块类型名称 ([#622](https://community.devsense.com/d/622-nonstandard-external-library-docblocks))。

## 1.13.10239 (2022年8月11日)





- 未知属性的代码诊断 (`PHP0416`)
  - 未知属性的快速修复（目前修复小错别字和大小写错误）
  - `stdClass` 和包含 `__get()` 魔术方法的类会被忽略（如 [PHP 8.2 RFC](https://wiki.php.net/rfc/deprecate_dynamic_properties) 中所指定）
- 自动导入（FQN）避免创建冲突名称
- `extends` 后的代码补全避免建议包含类自身
- 修复属性名称的大小写敏感性检查

## 1.12.10140 (2022年8月4日)




- 新增 `Go to Type Definition` 命令；在 `new` 表达式中导航到类型定义而非 `__construct`。
- PHPUnit 视图：修复了跟踪失败测试位置的问题（[#150](https://github.com/DEVSENSE/phptools-docs/issues/150#issuecomment-1192046307)）

## 1.12.10040 (2022年7月26日)




- 设置 `php.workspace.includePath`，允许指定要在 IntelliSense 中包含的附加目录。
- 改进工作区加载，更好地并行处理文件。

## 1.12.10022（2022年7月25日）




- 修复激活问题

## 1.12.9985（2022年7月20日）




- **PHPUnit 测试集成**
  - 新的 PHPUnit 测试用户界面
  - **显示内联失败消息**
  - 使用新界面**调试 PHPUnit 测试**
  - 期望值和实际值的**差异**
  - 更小的扩展
  - 避免依赖旧的 `ms-vscode.test-adapter-converter` **（可以卸载）**
  - 避免依赖旧的 `hbenl.vscode-test-explorer` **（可以卸载）**
- 优化的扩展加载，更小的安装包
- 根据类型提示建议新的参数名称
- 在新生成的文档注释中正确插入联合类型（在函数上方键入 `/**` 时）
- 生成的文档注释注解抛出的异常（`@throws` PHPDoc 标签）
- 处理外部更改，修复安装/更新 composer 包时的重新索引问题
- 在 PHPDoc 完成中显示所有类，在提交时将自动导入（根据设置 `php.format.autoimport`）
- 修复 **Alpine Linux Arm64** 平台
- 修复各种文本的 `phpTools.language` 设置（各种内置函数和常量的摘要）。
- 修复未使用的 `use` 警告列出两次的问题
- 修复变量在文档注释中的重命名重构。
- 不在模板文件中报告误用 `$this`
- 改进 `.phpstorm.meta` 文件中记录的函数后的自动完成。
- 改进在 trait 中用泛型类型注解的方法后的自动完成
- `php.format.autoimport-docblock` 设置用于配置在 Doc Block 中类型名称的自动完成，默认值为 `"FQN"`。

## 1.11.9762 (July 1, 2022)




- 修复了在 `enum` 的 case 之后的自动完成（未列出完成项）
- 修复了变量上的工具提示，解析后的类型名称被正确缩短

## 1.11.9761 (June 29, 2022)




- 修复错误 [#147](https://github.com/DEVSENSE/phptools-docs/issues/147)

## 1.10.9721 (June 25, 2022)




- 修复了在完成内建 `enum` 成员时语言服务器崩溃的问题。

## 1.10.9716 (2022年6月25日)




- 为内置的 `enum` 方法和属性提供 IntelliSense 支持。
- 改进了数组类型属性的类型推断。
- 识别并支持 Laravel 的实时 Facades，代码补全支持。
- Eloquent 的 Local Scopes 在代码补全中列出。
- 修复了当 `use` 用于未使用的文档注释时未使用的 `use` 的高亮问题。
- 修复了用 `@test` 文档注释标注的测试的测试资源管理器。

## 1.9.9585 (2022年6月7日)




- 推断 `@template` 类型，结合 `class-string<T>` 类型注解
- 自动识别一些非标准文件扩展名以解析为PHP文件（改善*Drupal*的代码补全）
- 修复保留类型名称（`self`，`parent`，`static`）后的补全
- 修复常量和类常量后的 `->` 语法（*PHP 8.1*）
- 修复表达式链中 `->` 和 `new` 后的补全
- 修复更改PHP版本

## 1.9.9479 (May 25, 2022)




- 改进在多核CPU上推断Laravel Facades
- 改进文档注释处理，支持更多phpstan和psalm的约定
- 改进对泛型类型和泛型`@mixin`类型的代码补全
- 修复在大型项目中可能发生的崩溃（修复StackOverflow）
- 修复在第三方扩展传递无效LSP协议数据时可能发生的补全问题
- 修复在处理多个并发请求时的断点问题
- 调试器稳定性改进

## 1.9.9277（2022年4月29日）




- **IntelliSense**
  - **支持泛型**
  - IntelliSense 能够处理专门化的类型名称
  - 模板化的类型根据绑定的泛型参数进行解析
  - 泛型类型从传递给 `new()` 的构造函数参数中推断
  - 工具提示显示泛型参数
  - IntelliSense 理解 `@template` 参数和扩展的 PHPDoc 语法（泛型、psalm、phpstan）
  - IntelliSense 补全用于泛型的特殊 PHPDoc 标签
  - 如果值没有绑定，代码补全使用模板 `of` 类型
  - 代码分析支持泛型
- 更新了 PHP 语法解析器，修复了 `instanceof` 语法
- 修复了安装/更新 composer 包后 IntelliSense 缺失项的问题
- 修复了 HTML/CSS/JS IntelliSense 的问题
- 修复了外部文件更改后 IntelliSense 的项目
- 默认包含 `zip` 和 `zlib` 的存根
- 提供用于第三方扩展的 API

## 1.8.8970 (2022年3月23日)




- 添加缺失的 `MYSQLI_` 常量
- 修复 PHPUnit 运行器；解析正确的 `phpunit` PHP 脚本
- 修复处理带空行和缩进的 HEREDOC 和 NEWDOC 语法
- 修复解析器以允许 PHP 8 构造函数属性中的 `readonly` 修饰符
- 修复 `phpTools.language` 设置，PHP 手册已正确本地化
- 未使用的 `use` 检查遵循 `@Method` PHPDoc 标签
- 修复在解析 PHP 二进制文件和相关 PHP 信息时的冻结问题
- `php.linkedEditing.variables`：设置以启用局部变量的链接编辑（默认为 `false`，需要启用 `editor.linkedEditing`）
- `editor.linkedEditing`：避免在删除整个变量名时出现错误编辑
- `editor.linkedEditing`：在变量名被删除后仍保持链接
- 调试器监听 IPv4 和 IPv6，支持可选启动配置 `"hostname"`
- 修复数组的调试器问题
- 即使没有匹配的 `php` 可执行文件，编辑器仍遵循 `php.version` 设置
- 检查 `composer.json` 以获取最低 PHP 版本，如果未设置 `php.version` 设置
- **web** 扩展显示并允许更改 PHP 语言级别

---

- 扩展不下载外部依赖项；使初始运行更快且可靠
- 扩展不期望系统上安装 `dotnet` 运行时
- 语言服务器支持增量文本编辑以降低协议开销
- 支持的新平台：`alpine-x64`，`win32-arm64`，`darwin-arm64`

## 1.7.8766 (2022年3月8日)




- 使用 `ctype` 书籍更新 IntelliSense
- 使用 STD 常量更新 IntelliSense
- 使用 `@ignore` 标记的函数不会在完成和签名帮助中列出
- `new` 之后的补全列表中也包含变量
- 优化

## 1.7.8717 (2022年3月4日)




- 修复语言服务器的稳定性可能出现的问题（使用 ORM 标记法时）
- `"php.debug.port"` 可以在工作区范围设置中设置。
- 修复调试测试；使用来自 `"php.debug.port"` 的正确端口或默认的 `9003`。
- Laravel 静态 Facades 在 IntelliSense 中被识别
- Laravel 类别名在 IntelliSense 中被识别
- 使用 PHPDoc 改进代码解析器

## 1.7.8637 (2022年2月26日)




- 修复了Web扩展加载问题

## 1.7.8627 (2022年2月25日)




- 调试器在一个或所有端口不可用时正确报告
- 修复IntelliSense中缺少的`E_`常量
- PHPUnit调试器遵循Xdebug端口设置"`php.debug.port`"而不是使用硬编码端口`9000`

## 1.6.8588 (2022年2月19日)




- 调试器 "exclude" 启动设置允许使用 `!` 前缀来否定路径，例如：
  ```json
  "exclude": ["!**/app/**", "!**/vendor/mypackage/**"]
  ```
- 如果没有可用的 Xdebug 端口，调试将不会启动
- 如果 Xdebug 端口无法使用，则会在调试输出面板中报告详细信息
- 安装：从其他位置下载依赖项
- IntelliSense 优先使用 PHPDoc 类型注释而不是类型提示（提供更具体的补全）
- Doctrine ORM 用于属性类型注释的赋值注释
- 语言服务器避免使用文件系统监视器，提高基于Unix系统上的性能 ([#521](https://community.devsense.com/d/521))
- 更小的安装包
- 设置 `"php.stubs"` 允许显式设置要包含在 IntelliSense、本地化手册和代码分析中的扩展名。
- 为局部变量添加了对**链接编辑** (`"editor.linkedEditing": true`) 的支持

---

- 新支持的平台：`web`

## 1.6.8479 (February 11, 2022)




- 修复了字符串值的预览
- 优化了文件解析

## 1.6.8448 (2022年2月10日)




- 代码分析显示了PHP 8.1 `readonly` 属性的错误声明
- 修复了虚拟PHP手册文件中的代码透镜（当导航到内置PHP使用前往定义（`F12`）时）
- 虚拟PHP手册显示为VS Code虚拟文档（不会在磁盘上创建临时文件）
- **PHPUnit运行和调试器** 设置 `phpunit.phpunit` 以指定phpunit二进制文件

## 1.6.8324 (2022年1月28日)




- **调试装饰**
- 扩展兼容性
- 枚举用例的代码透镜
- `php.debug.port` 和启动端口设置允许监听多个端口。默认是 `[9003, 9000]`。

## 1.5.8292 (2022年1月25日)




- 修复了调试工具提示和调试监视

## 1.5.8280 (2022年1月24日)




- **调试**启动改进，提供根据当前文件或工作区启动调试的所有选项
- 提供用于运行和调试PHP文件和项目的高级命令
- 增加了设置`php.debug.port`以指定默认的Xdebug端口
- 编辑器默认兼容PHP 8.1，除非另有指定
- 代码镜像小更新
- 修复关于缺失“php”的错误警告
- 修复扩展依赖问题
- 修复扩展激活时间问题

## 1.5.8204 (2022年1月17日) 预览版




- **代码镜像**
  - 引用，方法重写，trait 使用，类型实现，方法原型实现
  - 在引用窗口中查看引用
  - 启用/禁用的设置：`php.codeLens.enabled`。默认值为 `true`。
- 如果未为工作区设置 `php`，编辑器将从 `php.executables` 设置中选取定义最高的版本
- 改进了可空类型提示后的自动完成和工具提示
- 改进了对带有私有抽象函数的 `trait` 的代码分析
- 改进了对 `[]` 使用的代码分析
- 改进了关于全局代码中 `isset` 的代码分析
- 改进了对抽象方法未实现的分析
- 对 PHP 8.1 交集类型进行验证（检查标量的使用，检查使用的有效类型）
- 在函数头部的自动完成中添加了缺失的修饰符关键字
- 修复了 **测试**，允许运行所有测试（在 *测试* 面板中选择 `运行所有测试`）

## 1.4.8059 (2021年12月20日) 预览




- 检测到的 PHP 二进制文件可能有无效配置，如果用户愿意，PHP Tools 将报告警告并仍然使用这些二进制文件。
- 诊断报告在参数类型提示中不当使用 `static`
- 根据当前命名空间缩短工具提示中 PHP 8.1 交集类型内的类型名称
- 使用 PHP 8.1 语法更新颜色工具提示

## 1.4.8033 (2021年12月17日) 预览版




- 修复了*溢出到 double*问题的下划线位置
- 调试器尊重用户参数优先于其强制参数
- 在某些情况下避免建议添加`use`如果它已经存在（[#127](https://github.com/DEVSENSE/phptools-docs/issues/127)）
- 更新了 PHP 手册
- 更新了 PHP 8 属性中的代码补全
- 避免将 ByRef 问题报告为错误，改为报告为警告
- 折叠 HEREDOC 块
- 可能的修复 Windows 上现有`php`的解析
- PHP 8.1 交集类型（解析，解析）

> *注意：类型推断和工具提示尚未完全处理交集类型*

## 1.4.7597 (2021年9月30日) 预览版




- 更新了内置函数的推断类型分析
- 突出显示 `switch` 中的 `case`
- 修复了可能的堆栈溢出异常

## 1.4.7534 (2021年9月21日) 预览版




- 修复当代码包含巨大嵌套表达式时崩溃的问题
- 修复语言服务器协议
- 改进对 `array_pad()`，`array_fill()` 的代码分析
- 修复在 LValue 中链接使用 `[]` 的误报警告
- 内存优化

## 1.4.7520 (2021年9月19日) 预览版




- 内存优化
- 修复了当代码包含巨大嵌套表达式时崩溃的问题

## 1.4.7494 (2021年9月15日) 预览版




- 在工具提示中显示函数返回值摘要
- 修复重构操作
- 修复代码操作
- 修复PHPDoc生成器
- 优化协议

## 1.4.7449 (2021年9月7日) 预览版




- 改进 `$this` 的分析
- 改进未使用变量的错误报告
- 修复整个文档格式化
- 修复无变量的 `catch` 格式化
- 修复未指定调试端口时的偶发问题
- 内部性能改进针对 JSON 协议
- 修复无工作区的文档调试问题（*仅打开文件而无工作区或文件夹*）
- 更新 PHP 手册
- 修复 PHP 解析器 - `readonly` 按 PHP 版本正确处理

## 1.4.7295 (2021年8月17日) 预览版




- **PHP 8.1** 语法、代码感知和检查
  - 只读属性
  - 最终类常量
  - 初始化器中的新特性
  - 新的可调用语法
- 更新了 PHP 手册
- 修复了错误报告的废弃警告
- 修复了带有 'null' 类型提示的错误参数

## 1.4.7254 (2021年8月15日) 预览版




- **调试**
  - 允许组合启动
  - 允许同时进行更多调试会话
  - 无需指定 Xdebug 端口（`"port"` 启动配置）

## 1.4.6982 (2021年7月15日) 预览




- 当启用自动导入时，补全会显示可能命名空间中的所有可能类型
- 当自动导入并与现有别名冲突时，自动补全完全限定名
- 如果将进行自动导入，补全中显示 *(自动导入)*
- 补全更好地列出变量
- 优化
- 当有多种类型需要自动导入时，它们都会在补全列表中显示以供选择

## 1.4.6842 (2021年6月22日) 预览版




- 自动导入别名时完成
- 设置 `php.format.autoimport`
  - **自动导入选项**：在命名空间范围之外完成类型/函数/常量时自动导入别名
  - **fqn**：在完成时插入完全限定名
  - **none**：按原样插入名称
  - **hide**：在代码完成中不显示不可访问的符号
- 修复完全限定名称的代码操作的灯泡位置
- 在代码完成中划掉已弃用的符号

## 1.4.6822 (June 19, 2021) preview




- 更新了代码分析和代码补全
- 识别更多未记录的 `.phpstorm.meta.php` 结构 ([#102](https://github.com/DEVSENSE/phptools-docs/issues/102))
- 修复了 PHPUnit TestCase MockObject 类型分析 ([#102](https://github.com/DEVSENSE/phptools-docs/issues/102))
- 提供简化完全限定名称的代码操作 ([#88](https://github.com/DEVSENSE/phptools-docs/issues/88))

## 1.4.6762 (2021年6月7日) 预览版




- PHP 版本选择器 ([查看文档中的选择 PHP](https://docs.devsense.com/en/vscode/editor/php-version-select))
- `.editorconfig` 问题约定 ([查看文档中的问题](https://docs.devsense.com/en/vscode/problems#editorconfig))
- `"php.problems.scope"` 设置 (默认忽略 "vendor" 文件夹) ([查看文档中的问题](https://docs.devsense.com/en/vscode/problems#phpproblemsscope))
- 调试改进
- 异常处理 - 始终在致命错误时中断，可以选择是否在处理的错误/异常时中断

---

## 1.3.6645 (May 25, 2021) preview




- 调试修复和改进
- 调试用户体验改进

## 1.3.6632 (2021年5月21日) 预览版




- **测试资源管理器** 列出测试而不运行它们
- 测试资源管理器正确支持带数据集的测试
- 如果源代码被修改，测试将被标记为弃用（灰色显示）
- 优化了**调试协议**

## 1.3.6616（2021年5月21日）预览版




- 新的**测试资源管理器**（需要 `hbenl.vscode-test-explorer`）
- 调试已更新，支持多请求处理、稳定性增强、正确性
- 调试支持分离
- 优化 Xdebug 协议
- **PHP 8.1** 语法支持，`never` 返回类型，`enum`，八进制数字表示法
- 完成 `$this->` 后的静态方法
- 支持 `#[NoReturn]` 属性

---

## 1.2.6549 (2021年5月12日) 预览版




- 修复调试实现（意外调试会话关闭）
- 修复调试断点
- 优化 Xdebug 协议
- 修复 HEREDOC 解析器
- 修复特殊名称的命名参数分析
- 修复 PHP 8 解析和无效语法错误
- 优化性能

## 1.2.6469 (2021年4月24日) 预览版




- **排序用途**（PSR-12）的代码操作
- 自PHP 8.0以来报告大括号为弃用
- 支持远程文件系统
- 类型分析改进

## 1.2.6305 (April 04, 2021) preview




- 在状态栏中显示 PHP 版本，不带后缀
- macOS 热修复，下载运行时包

## 1.2.6273 (2021年3月30日) 预览




- **生成构造函数**的代码操作
- **getter/setter**的代码操作支持字段静态性
- 修复代码操作
- 更快的代码补全弹出窗口
- 更快的变量工具提示显示

## 1.2.6177 (2021年3月17日) 预览版




- 内存优化
- 修复 IA-32 架构上的 Node.JS 问题
- 修复模糊函数声明中的 `PHP0423` 问题
- 在自动完成中不列出匿名类的名称

## 1.2.6021 (Feb 17, 2021) preview




- 当用户在局部变量和全局变量上方输入 `/**` 时，为其生成 PHPDoc
- 更新了 PHP 手册，包含更多 PHP 8 声明
- 修复了 `::class` 和 `fn` 后的格式化显示
- 避免了一些错误报告的问题
- 修复 PHPDoc `@return` 标签中保留关键字的类型分析
- 工具提示中为内置类型关键字提供了更多详细信息
- 修复了从 Xdebug 首页下载的服务器的 DBGp 代理支持问题

## 1.2.5988 (2021年2月10日) 预览版




- 修复语言服务器崩溃（栈溢出异常）
- 更加宽容的问题验证
- 代码分析改进

## 1.2.5973 (Feb 08, 2021) 预览版




- 代码分析的整体改进，修复了 finally 块，受限常量不再报告
- 修复了命名空间中全局常量的重构和高亮冲突
- 性能提升
- （Linux, macOS）修复了在 VSCode 关闭或文件夹关闭后服务器未关闭的问题

## 1.2.5931 (2021年1月31日) 预览




- 重命名重构允许重命名动态名称
- 修复了 `__construct` 包含尾随逗号时的语言服务器崩溃
- 更新了 pcre 检查
- 类型分析改进，更少的错误警告
- 改进了对标准函数的分析
- 改进了对 try/catch 块的分析
- 对属性的 PHPDoc 类型注释不匹配更加宽容
- 类型检查查看特征和接口的子类型，不那么严格
- 修复了代码操作和快速修复

## 1.2.5887 (2021年1月23日) 预览版




- 重命名重构带预览功能
- `use` 组的美观打印
- 基于 .NET 5.0 构建（拥有 `.NET 5.0 Runtime` 可避免额外下载）
- 解决方法时处理子类型
- 处理 trait 用户，改进 trait 的分析以及子类型中方法的转到定义功能
- 改进代码分析和类型分析
- 避免大量错误警告
- 修正匿名类父类的转到定义功能

## 1.2.5843 (2021年1月18日) 预览版




- 源代码控制文件夹中的文件在更改时会被忽略（.git, .history, .svn）
- 修复状态栏中的PHP版本 - 只有在编辑PHP文件时才显示
- 优化
- 更新了PCRE检查
- 修复了文档最后的代码补全问题

## 1.2.5783 (Jan 04, 2021) 预览




- 支持 PHPDoc 中的 `@template` 注释
- 处理内联的 `@var` 注释
- 对于不明确的构造函数提供签名帮助（`new \ReflectionMethod`）
- PHPDoc 数组类型支持带有联合元素的注释（`array<A\B\C>`）
- PHPDoc 支持可为空类型注释（例如 `?int`）
- 优化
- 改进代码分析，避免一些误报
- 改进代码流分析，支持 isset()、is_resource() 和类型推断
- 改进对 lambda 函数使用变量的分析
- 允许并支持 CLI 特定的常量和变量的代码补全
- 更新 `.phpstorm.meta.php` 解析器以便进行类型推断
- 在使用 PHP 7.1+ 时，不支持 PHP4 风格的构造函数
- 修复匿名类的“转到实现”功能
- 修复生成器函数的返回检查
- 修复对 `__clone()` 魔术方法的检查，可为私有
- 修复对 `\SplObjectStorage` 的数组访问检查
- 修复对不可打印字符的大小写和数组键值重复性检查

---

## 1.1.5686 (Dec 23, 2020) preview




- 支持 `@mixin` 注释
- 支持返回类型为 `$this` 的 `@method` 注释
- 处理 PHPDoc 中的可空类型注释
- 修复 PHPDoc 块中类型名称的解析
- 修复一些错误报告的警告（主要是未知方法警告）
- 更新 pcre 检查
- 可安装在 linux-arm64
- 改进工具提示中的类型名称
- `match` 表达式的代码格式化
- 修复类声明的代码验证
- 更新集成的 PHP 手册

## 1.1.5620 (Dec 12, 2020) preview




- 语法检查遵循当前 PHP 版本，包括 8.0。
- 更多针对无效联合类型的快速修复
- 更新了 pcre 检查
- 工具提示中的类型名称呈现得更简短

## 1.1.5595 (Dec 04, 2020) preview




- 命名参数代码补全（PHP 8）
- 命名参数悬停信息
- 使用 `#[Deprecated]` 属性标注的函数在诊断中报告
- 匹配或未知命名参数的诊断（PHP 8）
- `iterable` 类型提示的诊断
- 可空类型的诊断
- 联合类型的诊断（PHP 8）
- 联合中的 `null` 类型名称（PHP 8）
- 改进的 `.phpstorm.metadata.php` 注释
- 支持 Xdebug 3.0 和 PHP 8.0 调试

## 1.1.5532 (Nov 21, 2020) 预览





- 更新 PSR-2 代码格式
- 警告 `PHP0415` 针对使用未定义常量
- 警告 `PHP0418` 针对使用未定义方法
- 当 `PHP0415` 可能是局部变量时提供代码修复
- 代码完成中的 doctrine 注解
- 修复 PHPDoc 中的类名自动完成
- 更新代码完成和分析中的全局常量
- 更新 PHP 手册翻译

---

## 1.0.5403 (Oct 28, 2020) preview




- 类属性分析
- 修复魔术方法的类型提示
- 稳定性修复

## 1.0.5342 (Oct 20, 2020) preview




- PHP 8 新的属性语法 `#[]`
- 更多代码建议
- 改进了在 PHPDoc 中使用时未使用的 `use` 诊断
- 改进了在输入时打开文档中的问题下划线
- `@suppress` 和 `@SuppressWarnings` PHPDoc 标签允许忽略类/函数中的指定警告
- 支持更多 PHPDoc 数组语法约定
- 改进了对 `isset()` 和 `new static()` 的分析

## 1.0.5264 (Sep 30, 2020) 预览版




- 修复了在变量代码补全中双美元符号 `$$` 的问题

## 1.0.5229 (Sep 22, 2020) preview




- 诊断和简易修复可以简化的名称
- 构造函数和私有函数中未使用参数的诊断
- 更新外部修改的文件 (`*.php`)

## 1.0.5153 (2020年8月28日) 预览版




- `@dataProvider` PHPDoc 属性；代码感知、导航、补全
- 实现缺失的抽象快速修复尊重原始 `public` 关键字
- 支持 PHP 8.0 空安全操作符
- 支持 PHP 8.0 `match` 构造（必须具备 PHP >=8.0 `phpExecutable`）
- 修复重叠问题的 `快速修复`
- 稳定性修复

## 1.0.5087 (Aug 17, 2020) preview




- 消除重复的快速修复
- 改进了在括号中包含的表达式的类型分析
- PHPDoc 中的未知类型名称提供快速修复
- 鼠标悬停显示函数是否返回 `null`（`void` 最终显示为 `null`）
- 方法的*转到实现*
- 为无效的基类提供快速修复
- `namespace` 关键字后的代码补全

## 1.0.5044 (2020年8月11日) 预览版




- 针对 PHPDoc 中未知类名的快速修复
- 删除不必要的 `use` 的快速修复
- `iterable` phpdoc 类型提示
- 在左侧状态栏加载状态指示器
- 当前 PHP 版本指示器在状态栏（右下角）
- 当代码更改时，工作区延迟重新分析（可通过 [`"php.problems.workspaceAnalysis": false`](https://docs.devsense.com/en/vscode/configuration#configuration-options) 禁用）

## 1.0.5029 (Aug 07, 2020) preview




- 支持“转到实现”
- 不再报告 `SonarSource.sonarlint-vscode` 作为不兼容
- 修复了在 `extends` 关键字后接口名称的“转到”功能
- 弃用的内容以删除线显示

## 1.0.5015 (Aug 06, 2020) preview




- `__construct`的“查找所有引用”包括类实例化
- “查找所有引用”性能
- 问题分析改进
- 改进了对内联PHPDoc类型提示的分析
- 某些与其他问题相关的问题未报告
- 解析器修复

## 1.0.4975 (July 29, 2020) preview




- 性能改进
- 问题分析改进
- 改善工作区加载
- 记录工作区加载失败情况

## 1.0.4934 (2020年7月19日) 预览版




- 独立的 `@deprecated` 不再被忽略
- 一些性能改进
- 修复了报告问题中的重复项
- 由于其他问题导致的一些问题未被报告
- 工作区加载和代码编辑改进

## 1.0.4908 (2020年7月13日) 预览版




- 更少的错误警告
- 改进了对 `static` 和属性的类型分析
- 支持 PHP 8.0 (Alpha 1) 语法
- 新增 PHP 8.0 兼容性警告
- 修复了 trait 成员的抽象实现
- 改进了使用制表符时的格式

## 1.0.4698 (May 19, 2020) preview




- 更好的 `use` 快速操作位置

## 1.0.4666 (2020年5月6日) 预览版




- 修复了在未安装 .NET Runtime (3.x 或 5.x) 的系统上的问题

## 1.0.4654 (2020年5月5日) 预览版




- 改进了所有测试的运行（现在在单个进程中运行）
- `@method` 中的 PHPDoc 类型提示遵循当前命名空间
- 箭头函数中的局部变量从父作用域使用，并正确注释

## 1.0.4608 (2020年4月17日) 预览版




- 修复了`在控制台中启动当前脚本`的配置片段
- PHP脚本中的HTML工具提示
- `<` 触发HTML完成
- PCRE模式检查（在`preg_*`函数中）
- 支持具有可变参数的PHPDoc `@method`
- 未使用的`use`高亮遵循自定义PHPDoc标签
- 测试资源管理器修复：
  - 测试结束后调试会话关闭
  - 测试用例可在无额外配置下进行调试
  - 修复测试运行时的异常

## 1.0.4394 (2020年1月23日) 预览版




- 修复变量自动补全（`$` 前缀不再重复）

## 1.0.4277 (2019年12月10日) 预览版




- 改进了对 `finally` 块的代码流分析
- 如果系统上安装了 `dotnet` 3.1，则加以利用
- 对稳定性问题进行小修复和更新

## 1.0.4229 (2019年11月22日) 预览版




- `实现抽象` **代码操作** 和 **快速修复**（接口和抽象成员）
- 为字段和多个字段提供 `添加 getter/setter` **代码操作**
- 更新稳定性问题

## 1.0.4187 (2019年11月10日) 预览版




- 代码编辑器修复（在保存时格式化、粘贴时格式化时发生）
- PHPDoc 内的补全

## 1.0.4168 (2019年11月4日) preview




- 改进了文档/工作区中的符号列出
- 搜索时列出以 `$` 为前缀的属性
- 导航到 trait 的使用位置

## 1.0.4145 (2019年10月24日) 预览版




- 检查未实现函数的问题
- 检查traits的问题
- 改进的工具提示和性能
- 更新内置PHP手册
- 调试器以人性化方式报告常见问题

## 1.0.4009 (2019年9月23日) 预览版




- 工具提示中的 `{@link}` 显示为超链接
- `{@inheritdoc}` 根据 PHPDoc 规范进行替换。
- 更新了 blade 模板编辑器（`@section`、`@yield`）和格式修复
- 内嵌 HTML 修复
- 稳定性修复，改进了内部错误日志记录
- 改进了问题报告

## 1.0.3951 (2019年9月9日) 预览版




- 生成的PHPDoc遵循类型提示
- 生成的PHPDoc正确处理可为空类型
- 修复语言服务器崩溃
- 避免在运行`composer install|update`时生成`rg.exe`（修复系统冻结问题）

## 1.0.3936 (2019年9月5日) 预览版




- 工作区中的 PHAR 文件会被解析
- **代码补全** 包括来自 PHAR 文件的声明
- **转到定义** 支持 PHAR 文件中的内容
- **导航** 穿过 PHAR 文件中的条目
- PHAR 文件中声明的**签名帮助**和**工具提示**
- 小错误修复和改进

## 1.0.3774 (August 1, 2019) preview




- 已格式化的类型属性
- `use`之后的补全根据类名进行过滤
- 从 Xdebug 获取长数据

## 1.0.3748 (2019年7月24日) 预览版




- 当前命名空间或使用中不可用的类/接口/特性不会在代码补全中列出
- 支持代码补全和类型分析中的动态类别名（`class_alias()`和Joomla注册的别名）
- blade块中的PHP代码（`.blade.php`）（不包括语法高亮）
- 改进了通过引用传递的参数的类型分析
- 修复了启用`Format on Paste`时的粘贴问题（HTML被损坏）

## 1.0.3703 (2019年7月17日) 预览




- 性能优化
- `php.problems.workspaceAnalysis` 设置用于启用/禁用工作区范围的问题分析
- 数组解包类型检查

**PHP 7.4 支持**

- 支持 PHP 7.4（箭头函数、类型属性、扩展数组、`??=` 操作符、数字中的下划线）
- 在使用 PHP < 7.4 时报告 PHP 7.4 的功能
- PHP 7.4 功能分析、类型分析、问题分析
- 扩展数组类型检查

## 1.0.3645 (2019年7月11日) 预览




- 改进了项目加载和后台分析
- 处理`.phpstorm.meta.php`（版本2016.2+）
- IoC的代码补全和分析
- 修复了可为空类型的格式问题
- 格式化美化打印开括号`{`
- 格式化代码风格默认为`PSR-2`

## 1.0.3603 (2019年7月8日) 预览版




- 修复了某些警告消失后几秒钟又出现的问题
- 改进了打开/关闭文档时的 CPU 使用
- 修复了 `?:` 和 `::` 周围的格式
- 改进了代码分析评估
- 对未初始化变量使用的分析更不严格
- `use` 后的补全会获得完全限定名称

## 1.0.3593 (2019年7月5日) 预览版




- 魔术方法诊断
- 重复函数参数诊断
- 改进数字类型分析
- 启动调试器增强
- PSR-2 格式化程序修复

## 1.0.3574 (2019年7月2日) 预览版




- 改进了对 `explode()`、`microtime()`、Oxid 框架的类型分析
- `catch` 变量诊断和分析

## 1.0.3547 (June 27, 2019) preview




- 格式化器改进
- 支持 DBGP 代理
- 改进的未使用变量诊断

## 1.0.3525 (2019年6月24日) 预览




- 匿名函数类型分析
- 使用 PHPDoc 注释的匿名函数
- 工具提示中的匿名函数详情
- 带有函数返回类型的签名帮助
- 显示未使用变量
- 加载项目性能、响应能力

## 1.0.3507 (2019年6月22日) 预览版




- 修正了在代码格式化时未命名文档数量增加的问题
- 类型分析改进
- 初步支持 dbgp 代理

## 1.0.3483 (June 17, 2019) preview




- 更新了 PHP 手册
- 验证传递给 `define()` 的值
- 验证在 PHP >= 7.3 上使用 `define()`

## 1.0.3471 (2019年6月12日) 预览




- 支持日志断点
- `php.format.codeStyle` 可以在工作区范围内设置
- 代码格式修正，打开标签后的缩进，新行上的代码块
- `html`+`php` 格式修正，修复重叠范围错误

## 1.0.3435 (2019年5月28日) 预览版




- 修复禁用断点的问题
- 优化调试协议

## 1.0.3428 (May 27, 2019) preview




- 更新了PHP手册以涵盖最新的PHP 7.3和PHP 7.4结构
- 更新了自述文件

## 1.0.3386 (2019年5月9日) 预览版




- 禁用警告 PHP0424 当在 foreach 中传递对象时
- 分析 lambda 函数中的使用参数
- 小的代码导航修复
- 小的代码格式修复

## 1.0.3348 (Apr 23, 2019) preview




- 签名助手已修复，显示正确的参数
- 修复了在没有 `dotnet` 时运行扩展的问题
- 兼容 `dotnet` 3.0

## 1.0.3241 (Mar 4, 2019) preview




- 使用参数名称生成PHPDoc

## 1.0.3230 (Feb 27, 2019) 预览版




- 插入带有占位符的 PHPDoc 块（代码片段）
- PHPDoc 标签代码片段
- PHP 兼容性警告
- 修复了文件删除后警告不消失的问题
- 修复了 `die()` 构造的格式化打印问题
- 修复了函数头和属性的格式化问题

## 1.0.3202 (Feb 20, 2019) 预览版




- 更新了 PHP 手册
- 键入时格式化（`;` 和 `}`）
- 格式配置文件 `Off`
- 当代码语法无效时不应用格式化

## 1.0.3185 (Feb 14, 2019) 预览版




- 在 PHPDoc 中代码补全 PHPDoc 关键字（在 `@` 后）
- 针对 PHPDoc 中拼写错误和未知类型名称的代码操作

## 1.0.3174 (2019年2月12日) 预览版




- 当适用时，添加 `use ;` 的代码操作
- 在必要时完全限定类型名称的代码操作
- 用户输入 `/**` 时生成 `PHPDoc` （必须启用 `formatOnType`）
- 选择格式化
- 本地化消息 - en, de, ja, tz, es

## 1.0.3058 (Dec 30, 2018) preview




- 改进的代码格式化
- 一些文本本地化为德语

## 1.0.3031 (2018年12月3日) 预览版




- 折叠会收起内部范围
- 格式化代码风格设置 `php.format.codeStyle`
- 对具有多个 `@var`/`@global` 标签的局部变量进行 PHPDoc 注释
- 如果适用，代码建议添加 `$this->`

## 1.0.3003 (2018年11月26日) 预览版




- 为未知类错误提供代码建议
- 不必要的 `use` 指令呈现为淡出效果
- `F10` 和 `F11` 开始调试并停止在入口
- `exclude` 启动配置 - 这些模式将在单步调试时跳过
- 调试器允许设置变量或属性值
- 调试器支持长字符串
- 调试器支持大数组的分页
- 测试资源管理器优化
- 生成的文件不包含在用户的工作空间中
- 测试资源管理器仅显示用户的测试，仅当根目录中没有 `phpunit.xml` 时才列出递归目录中的所有测试

## 1.0.2930 (2018年11月3日) 预览版




- 显示语言设置 `phpTools.language` 可以在不重新加载工作区的情况下更改
- 更改设置 `php.problems.exclude` 会更新问题窗口
- 在编辑器外部更改的文件会被更新
- 稳定性修复

## 1.0.2915 (2018年10月30日) 预览版




- 调试器允许检查堆栈帧和局部变量值
- 实验性功能：处理设置 `files.exclude`
- 实验性功能：设置 `php.problems.exclude` 允许忽略指定文件夹以及所有或指定的问题代码
- 在 `<?` 之后不完成项
- 光标下引用的高亮优化

## 1.0.2895 (Oct 23, 2018) preview




- 项目问题在工作区加载后更新
- 不报告一些错误警告
- `pathMappings` 启动配置
- 修复：在 Unix 系统上关闭语言服务器进程
- 修复：处理大型混合 HTML/JS/CSS/PHP 代码
- 新对象的签名帮助
- 内存和性能优化
- 稳定性修复
- 项目启动优化
- 所有括号的代码折叠

## 1.0.2802 (2018年10月11日) 预览版




- 选项以离线方式激活许可证/请求试用
- 选项以静音缺少PHP的警告
- 测试不会自动加载和运行（需要启用`autorun`或点击`reload`/`start`）
- 调试监视工具提示提供可扩展的对象属性
- 更详细的关于PHP和用于调试/测试的Xdebug输出日志
- 即使没有`launch.json`配置，按`F5`也会启动当前脚本的调试
- 不提供基本的在`:`后的代码补全（但包括`::`）
- 代码补全处理模棱两可的方法声明

## 1.0.2765 (Oct 8, 2018) preview




- 工作区中的符号功能。
- 处理映射到 `php` 语言的所有文件。
- 代码完成改进。

## 1.0.2738 (Oct 3, 2018) preview




- 测试资源管理器检测到 phpunit.xml.dist 即可启用
- 代码补全更好地处理了不明确的类型
- 如果没有正常的打开标签 `<?php`，则允许短打开标签 `<?`
- 更新了自述文件和文档
- 在 $ 后重新启用补全（修复了 VSCode 最近的更新）

## 1.0.2681 (Sep 27, 2018) 预览版




- 请求试用许可证的选项
- 从 CDN 下载依赖项
- 更新了扩展的发布者 ID

## 1.0.2590 (Sep 14, 2018) preview




- 在 ->, $, \, :: 后触发代码补全
- 代码块折叠，注释，PHPDoc 和区域
- 提供语言服务器
    - 代码补全
    - 悬停
    - 格式化
    - 代码结构
    - 签名帮助
    - 查找所有引用
    - 导航
    - 转到定义
    - 重构
    - 高亮
- 代码分析和验证
- 调试支持
    - 监视
    - 鼠标悬停调试监视
    - 断点
    - UNC 路径
    - 路径映射
    - 远程调试，控制台，内置服务器
- 工作空间
- UNC 路径
- 内置 PHP 服务器
- PHPUnit 测试资源管理器
    - 实时测试
    - 测试调试器
    - 测试浏览器
- VS Code 的 PHP Tools 初始版本
