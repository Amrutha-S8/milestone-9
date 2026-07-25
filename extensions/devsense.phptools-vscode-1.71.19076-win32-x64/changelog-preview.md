## 1.71.19076 (July 16, 2026)

### Code Actions

Newly, the editor provides quick fix for deprecated symbols annotated with `#[Deprecated( ..., replacement: ... )]` attribute.

### Minor Improvements

- `@property` definition is respected if there is same property declared as `private`. [#1055](https://github.com/DEVSENSE/phptools-docs/issues/1055)
- PHPStans' syntax for array offset in PHPDoc type hints, i.e. `TArray['key']`, is recognized and respected. Type inferring in case of generics is still limited though. [#632](https://github.com/DEVSENSE/phptools-docs/issues/632)
- Arguments validation and parameter inlay hints for indirect function calls.
- Quick fix for unknown class name within `instanceof` expression.
- Added some commonly used snippets to code completion.
- Code action to implement interface (_Implement abstract members_) implements properties as well.

## 1.71.19014 (June 22, 2026)

### Minor Improvements

- Valid callback function checks now respect that callbacks can also be a `string`, not just a function name. [#1053](https://github.com/DEVSENSE/phptools-docs/issues/1053)
- Check for property set visibility. [#2589](https://community.devsense.com/d/2589)
- Code lens references to `__construct` now count references to `new` as well (consistent with _Find All References_ behavior). [#1050-comment](https://github.com/DEVSENSE/phptools-docs/issues/1050#issuecomment-4742244665)
- Fixed false warnings in HEREDOC strings containing escaped newline characters. [#2577](https://community.devsense.com/d/2577), [#1053](https://github.com/DEVSENSE/phptools-docs/issues/1053), [#2591](https://community.devsense.com/d/2591). This update also adds precise error reporting inside HEREDOC text, so the exact line with incorrect indentation is underlined.

### Debugger

- Virtual Exception Support: Added native support for Xdebug virtual exceptions. The debugger now automatically resolves and displays exception details and stack traces, while keeping the `$__EXCEPTION` variable accessible in the Variables view for deep inspection Requires Xdebug 3.5 or later.

  ![$__EXCEPTION variable in Locals](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/debug/img/virtual-exception.png)

- Stack Trace Formatting: Exception stack traces are now automatically parsed into clickable links, allowing for direct navigation to the source code.

## 1.71.18989 (June 16, 2026)

### IntelliSense

- Added code completion of method names in the array-type callable syntax.
- _Find all references_ to a string literal lists all occurences of that text in user's code.
- _Find all references_ to known string values (e.g. WordPress Hook names). [#2588](https://community.devsense.com/d/2588)
- Tooltip of a function in array-type callable syntax.
- Validation and navigation of a function name in string-type and array-type callables.

  ![Array Callback Intelligence](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/array-callback-intelligence.png)

  **Array-like callbacks** and **String-like callbacks** are validated, get contextual completion, navigation, semantic highlighting, rename refactoring, and tool-tips with the refered function details.

### WordPress

- Functions and classes from _WordPress_ stubs have correct links to the documentation. [#1039](https://github.com/DEVSENSE/phptools-docs/issues/1039)
- _Navigation_ to a WordPress hook invocation.
- _Find all references_ to a WordPress hook.
- Tool tip denotates the type of the string value (e.g. `(WordPress Hook) 'wp_head'`).

![WordPress Hooks](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/frameworks/img/wp-hook-references.png)

### PHP Manual

The entire multi-language PHP manual has been updated with new PHP stubs, additional translations, and previously undocumented PHP functions and classes. These updates improve code intelligence, code analysis, and code actions.

![Chinese PHP Manual](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/php-manual-chinese.png)

### Minor Improvements

- Not showing refactoring hints, if code actions are disabled. [#1038](https://github.com/DEVSENSE/phptools-docs/issues/1038)
- `is_null()` code action adds parentheses if they are necessary.
- _Laravel_: Improves navigation to controller's action from `Route` definition in a group declaration.
- Functions returning uninitialized variables are treated as they return `mixed`. [#1045](https://github.com/DEVSENSE/phptools-docs/issues/1045)
- Unknown global variables in lambda's `use()` are not reported. [#1044](https://github.com/DEVSENSE/phptools-docs/issues/1044)
- Respects tentative types, and fixes false warnings in class overrides. [#1043](https://github.com/DEVSENSE/phptools-docs/issues/1043)
- Improves `BcMath` support. [#2559](https://community.devsense.com/d/2559)
- `namespace` symbol in the _Outline_ view is shown according to the `"outline.showNamespaces"` setting. [#2578](https://community.devsense.com/d/2578)

  ![Outline with Namespaces](https://raw.githubusercontent.com/DEVSENSE/phptools-docs/refs/heads/master/docs/vscode/imgs/outline-with-namespace.png)

## 1.70.18915 (May 27, 2026)

### IntelliSense & Diagnostics

- Type inferring respects arithmetic operators overriden by `BcMath\Number`. [#2559](https://community.devsense.com/d/2559)
- Respects standalone `@disregard` tag (alias to `@suppress`) with no error codes. The tag above a statement or function will cause the editor to ignore all warnings.
- Improves IntelliSense after a variable annotated with a generic template type. [#2565](https://community.devsense.com/d/2565)
- Respects ambiguity in type inferrence within array access and foreach loop. [#2522](https://community.devsense.com/d/2522)
- Warnings corresponding to the unused `$_` are ignored by default as `$_` is considered to be a dummy variable. [#2570/2](https://community.devsense.com/d/2570-at-suppress-is-not-working-may-2026/2)
- Fixed check for `@require-extends`. [#2572](https://community.devsense.com/d/2572)

### UI

- `"hostname"` `launch.json` property is recognized by VSCode. [#2551/3](https://community.devsense.com/d/2551/3)
- Newly changelog is shown in Chinese, if VSCode's Display Language is Chinese.

## 1.70.18851 (May 13, 2026)

### Improvements

- The `"numeric-string"` type is now respected; implicit conversions from numeric strings no longer produce unnecessary warnings.
- Various control-flow analysis cleanups and stability improvements.

### PHPDoc

- Parsing nested PHPDoc tags is more tolerant, improving robustness of PHPDoc parsing.
- Fixed matching of `@global` occurrences.
- Fixed type name code completion in PHPDoc tags. [#892 (comment)](https://github.com/DEVSENSE/phptools-docs/issues/892#issuecomment-4422799460)

### IntelliSense

- `$GLOBALS['NAME']` is now handled more specifically in mouse hover and refactoring features.
- Fixed type inference for dynamic properties when an array has more than one element type.

### WordPress

- Added compatibility with more non-standard WordPress type syntax.
- Extended support for structured WordPress type syntax conventions.

## 1.70.18840 (May 9, 2026) [...]
## 1.70.18740 (April 7, 2026) [...]
## 1.69.18673 (March 26, 2026) [...]
## 1.68.18590 (March 11, 2026) [...]
## 1.67.18520 (Feb 17, 2026) [...]
## 1.67.18502 (Feb 13, 2026) [...]
## 1.67.18497 (Feb 11, 2026) [...]
## 1.66.18408 (Jan 29, 2026) [...]
## 1.66.1837 (Jan 26, 2026) [...]
## 1.66.18374 (Jan 24, 2026) [...]
## 1.65.18327 (Jan 14, 2026) [...]
## 1.64.18270 (Dec 30, 2025) [...]
## 1.63.18172 (Dec 3, 2025) [...]
## 1.63.18152 (Nov 27, 2025) [...]
## 1.62.18097 (Nov 12, 2025) [...]
## 1.62.18042 (October 30, 2025) [...]
## 1.62.17969 (October 9, 2025) [...]
## 1.61.17926 (September 23, 2025) [...]
## 1.60.17873 (Sep 2, 2025) [...]
## 1.60.17845 (Aug 23, 2025) [...]
## 1.60.17803 (Aug 14, 2025) [...]
## 1.59.17706 (July 29, 2025) [...]
## 1.59.17685 (July 23, 2025) [...]
## 1.59.17674 (July 18, 2025) [...]
## 1.59.17515 (June 23, 2025) [...]
## 1.59.17478 (June 15, 2025) [...]
## 1.58.17223 (May 2, 2025) [...]
## 1.57.17158 (April 11, 2025) [...]
## 1.57.17031 (March 25, 2025) [...]
## 1.57.16971 (March 12, 2025) [...]
## 1.56.16884 (February 19, 2025) [...]
## 1.56.16853 (February 12, 2025) [...]
## 1.55.16740 (January 22, 2025) [...]
## 1.55.16685 (January 15, 2025) [...]
## 1.54.16574 (December 23, 2024) [...]
## 1.54.16480 (December 10, 2024) [...]
## 1.53.16379 (November 19, 2024) [...]
## 1.53.16338 (November 12, 2024) [...]
## 1.52.16273 (October 30, 2024) [...]
## 1.52.16226 (October 21, 2024) [...]
## 1.51.16099 (September 26, 2024) [...]
## 1.51.15986 (September 10, 2024) [...]
## 1.50.15906 (August 20, 2024) [...]
## 1.50.15872 (August 13, 2024) [...]
## 1.49.15728 (July 8, 2024) [...]
## 1.48.15635 (June 16, 2024) [...]
## 1.47.15512 (May 28, 2024) [...]
## 1.46.15409 (May 9, 2024) [...]
## 1.45.15272 (April 11, 2024) [...]
## 1.45.15260 (April 8, 2024) [...]
## 1.45.15192 (March 26, 2024) [...]
## 1.45.15145 (March 14, 2024) [...]
## 1.45.15061 (February 27, 2024) [...]
## 1.44.14997 (February 14, 2024) [...]
## 1.44.14950 (February 7, 2024) [...]
## 1.44.14925 (February 5, 2024) [...]
## 1.43.14858 (January 24, 2024) [...]
## 1.43.14756 (January 15, 2024) [...]
## 1.42.14626 (December 30, 2023) [...]
## 1.42.14434 (December 12, 2023) [...]
## 1.41.14263 (November 14, 2023) [...]
## 1.40.14103 (October 18, 2023) [...]
## 1.39.13943 (September 20, 2023) [...]
## 1.38.13918 (September 15, 2023) [...]
## 1.38.13779 (September 1, 2023) [...]
## 1.38.13759 (August 30, 2023) [...]
## 1.37.13534 (August 4, 2023) [...]
## 1.36.13417 (July 1, 2023) [...]
## 1.35.13327 (June 20, 2023) [...]
## 1.34.13295 (June 15, 2023) [...]
## 1.34.13120 (May 5, 2023) [...]
## 1.33.12934 (April 8, 2023) [...]
## 1.33.12924 (April 05, 2023) [...]
## 1.32.12895 (March 28, 2023) [...]
## 1.31.12821 (March 20, 2023) [...]
## 1.31.12740 (March 4, 2023) [...]
## 1.30.12484 (February 10, 2023) [...]
## 1.30.12450 (February 9, 2023) [...]
## 1.30.12417 (February 7, 2023) [...]
## 1.29.12304 (January 29, 2023) [...]
## 1.28.12200 (January 21, 2023) [...]
## 1.27.12010 (January 9, 2023) [...]
## 1.26.11866 (January 3, 2023) [...]
## 1.26.11753 (December 28, 2022) [...]
## 1.25.11652 (December 21, 2022) [...]
## 1.25.11537 (December 11, 2022) [...]
## 1.24.11420 (December 1, 2022) [...]
## 1.23.11234 (November 10, 2022) [...]
## 1.22.11089 (October 31, 2022) [...]
## 1.21.10985 (October 23, 2022) [...]
## 1.20.10937 (October 19, 2022) [...]
## 1.19.10893 (October 16, 2022) [...]
## 1.18.10692 (September 30, 2022) [...]
## 1.17.10641 (September 26, 2022) [...]
## 1.15.10535 (September 14, 2022) [...]
## 1.14.10471 (September 7, 2022) [...]
## 1.13.10390 (August 30, 2022) [...]
## 1.13.10378 (August 29, 2022) [...]
## 1.13.10301 (August 16, 2022) [...]
## 1.13.10239 (August 11, 2022) [...]
## 1.12.10140 (August 4, 2022) [...]
## 1.12.10040 (July 26, 2022) [...]
## 1.12.10022 (July 25, 2022) [...]
## 1.12.9985 (July 20, 2022) [...]
## 1.11.9762 (July 1, 2022) [...]
## 1.11.9761 (June 29, 2022) [...]
## 1.10.9721 (June 25, 2022) [...]
## 1.10.9716 (June 25, 2022) [...]
## 1.9.9585 (June 7, 2022) [...]
## 1.9.9479 (May 25, 2022) [...]
## 1.9.9277 (April 29, 2022) [...]
## 1.8.8970 (March 23, 2022) [...]
## 1.7.8766 (March 8, 2022) [...]
## 1.7.8717 (March 4, 2022) [...]
## 1.7.8637 (February 26, 2022) [...]
## 1.7.8627 (February 25, 2022) [...]
## 1.6.8588 (February 19, 2022) [...]
## 1.6.8479 (February 11, 2022) [...]
## 1.6.8448 (February 10, 2022) [...]
## 1.6.8324 (January 28, 2022) [...]
## 1.5.8292 (January 25, 2022) [...]
## 1.5.8280 (January 24, 2022) [...]
## 1.5.8204 (January 17, 2022) preview [...]
## 1.4.8059 (December 20, 2021) preview [...]
## 1.4.8033 (December 17, 2021) preview [...]
## 1.4.7597 (September 30, 2021) preview [...]
## 1.4.7534 (September 21, 2021) preview [...]
## 1.4.7520 (September 19, 2021) preview [...]
## 1.4.7494 (September 15, 2021) preview [...]
## 1.4.7449 (September 7, 2021) preview [...]
## 1.4.7295 (August 17, 2021) preview [...]
## 1.4.7254 (August 15, 2021) preview [...]
## 1.4.6982 (July 15, 2021) preview [...]
## 1.4.6842 (June 22, 2021) preview [...]
## 1.4.6822 (June 19, 2021) preview [...]
## 1.4.6762 (June 07, 2021) preview [...]
## 1.3.6645 (May 25, 2021) preview [...]
## 1.3.6632 (May 21, 2021) preview [...]
## 1.3.6616 (May 21, 2021) preview [...]
## 1.2.6549 (May 12, 2021) preview [...]
## 1.2.6469 (April 24, 2021) preview [...]
## 1.2.6305 (April 04, 2021) preview [...]
## 1.2.6273 (March 30, 2021) preview [...]
## 1.2.6177 (March 17, 2021) preview [...]
## 1.2.6021 (Feb 17, 2021) preview [...]
## 1.2.5988 (Feb 10, 2021) preview [...]
## 1.2.5973 (Feb 08, 2021) preview [...]
## 1.2.5931 (Jan 31, 2021) preview [...]
## 1.2.5887 (Jan 23, 2021) preview [...]
## 1.2.5843 (Jan 18, 2021) preview [...]
## 1.2.5783 (Jan 04, 2021) preview [...]
## 1.1.5686 (Dec 23, 2020) preview [...]
## 1.1.5620 (Dec 12, 2020) preview [...]
## 1.1.5595 (Dec 04, 2020) preview [...]
## 1.1.5532 (Nov 21, 2020) preview [...]
## 1.0.5403 (Oct 28, 2020) preview [...]
## 1.0.5342 (Oct 20, 2020) preview [...]
## 1.0.5264 (Sep 30, 2020) preview [...]
## 1.0.5229 (Sep 22, 2020) preview [...]
## 1.0.5153 (Aug 28, 2020) preview [...]
## 1.0.5087 (Aug 17, 2020) preview [...]
## 1.0.5044 (Aug 11, 2020) preview [...]
## 1.0.5029 (Aug 07, 2020) preview [...]
## 1.0.5015 (Aug 06, 2020) preview [...]
## 1.0.4975 (July 29, 2020) preview [...]
## 1.0.4934 (July 19, 2020) preview [...]
## 1.0.4908 (July 13, 2020) preview [...]
## 1.0.4698 (May 19, 2020) preview [...]
## 1.0.4666 (May 06, 2020) preview [...]
## 1.0.4654 (May 05, 2020) preview [...]
## 1.0.4608 (April 17, 2020) preview [...]
## 1.0.4394 (January 23, 2020) preview [...]
## 1.0.4277 (December 10, 2019) preview [...]
## 1.0.4229 (November 22, 2019) preview [...]
## 1.0.4187 (November 10, 2019) preview [...]
## 1.0.4168 (November 4, 2019) preview [...]
## 1.0.4145 (October 24, 2019) preview [...]
## 1.0.4009 (September 23, 2019) preview [...]
## 1.0.3951 (September 9, 2019) preview [...]
## 1.0.3936 (September 5, 2019) preview [...]
## 1.0.3774 (August 1, 2019) preview [...]
## 1.0.3748 (July 24, 2019) preview [...]
## 1.0.3703 (July 17, 2019) preview [...]
## 1.0.3645 (July 11, 2019) preview [...]
## 1.0.3603 (July 8, 2019) preview [...]
## 1.0.3593 (July 5, 2019) preview [...]
## 1.0.3574 (July 2, 2019) preview [...]
## 1.0.3547 (June 27, 2019) preview [...]
## 1.0.3525 (June 24, 2019) preview [...]
## 1.0.3507 (June 22, 2019) preview [...]
## 1.0.3483 (June 17, 2019) preview [...]
## 1.0.3471 (June 12, 2019) preview [...]
## 1.0.3435 (May 28, 2019) preview [...]
## 1.0.3428 (May 27, 2019) preview [...]
## 1.0.3386 (May 9, 2019) preview [...]
## 1.0.3348 (Apr 23, 2019) preview [...]
## 1.0.3241 (Mar 4, 2019) preview [...]
## 1.0.3230 (Feb 27, 2019) preview [...]
## 1.0.3202 (Feb 20, 2019) preview [...]
## 1.0.3185 (Feb 14, 2019) preview [...]
## 1.0.3174 (Feb 12, 2019) preview [...]
## 1.0.3058 (Dec 30, 2018) preview [...]
## 1.0.3031 (Dec 3, 2018) preview [...]
## 1.0.3003 (Nov 26, 2018) preview [...]
## 1.0.2930 (Nov 3, 2018) preview [...]
## 1.0.2915 (Oct 30, 2018) preview [...]
## 1.0.2895 (Oct 23, 2018) preview [...]
## 1.0.2802 (Oct 11, 2018) preview [...]
## 1.0.2765 (Oct 8, 2018) preview [...]
## 1.0.2738 (Oct 3, 2018) preview [...]
## 1.0.2681 (Sep 27, 2018) preview [...]
## 1.0.2590 (Sep 14, 2018) preview [...]

