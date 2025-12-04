---
navigation_title: Word choice
description: Recommendations for choosing the right words in your documentation.
---

# Word choice

Find the right term to use in your technical documentation. Apply this guidance as follows:

- **Preferred**:  This term is recommended.

- **Use with caution**:  This term might be ambiguous.
Make sure you are using the term correctly.

- **Avoid**: This term might be offensive or non-inclusive.
Whenever possible, use the alternate suggestion, or a more specific term.

:::{tip}
Use the [Vale linter](/contribute-docs/vale-linter.md) to check for style issues while writing documentation. Vale automatically flags common style guide violations, so you can catch and fix issues before publishing.
:::

---

| Word | Status | Usage notes |
| ---- | ------ | ----------- |
| **abort** | 🔴 Avoid | This word can be offensive. Use _shut down,_ _cancel,_ or _stop_ instead. |
| **above** | 🟠 Use with caution | Don't use to refer to a postion. Directional language does not meet accessibility requirements.|
| **add** | 🟢 Preferred | Use for establishing a new relationship.  Often used in create-then-add scenarios: _Create a dashboard, then add a visualization_. _Remove_ is the correct opposite. |
| **app**, **application**| 🟠 Use with caution | Use only when needed for clarity.  Otherwise, a Kibana app name can stand alone.  _App_ is a well-known abbreviation for _application_ and is preferred. |
| **begin** | 🟠 Use with caution | Similar to _start_, using _begin_ depends on the context. _Begin a procedure,_ _begin an analysis,_ or _begin an installation_ are common phrases. Similarly, _start a program,_ _start an engine,_ or _start a timer_ are frequently used.  _Start_ is considered less formal than _begin_. _End_ is the correct opposite of _begin_.|
| **below** | 🟠 Use with caution | Don't use to refer to a position. Directional language does not meet accessibility requirements.|
| **blacklist** | 🔴 Avoid | This word has roots in racism. Use _blocklist_ instead. |
| **boot** | 🔴 Avoid | Use _start_ or _run_ instead. |
| **can** | 🟢 Preferred | Use to convey permission. |
| **cancel** | 🟢 Preferred | Use to stop an action without saving pending changes. |
| **cannot**, **can't** | 🟢 Preferred | Use to indicate you don't have the ability to do something.  Often confused with _unable_. |
| **choose** | 🔴 Avoid | Use _select_ instead. |
| **click** | 🟠 Use with caution | OK when describing mouse actions. Otherwise, use verbs that work with multiple devices, such as _select_.   |
| **clone** | 🟠 Use with caution | Use when creating a copy that is linked to the original. Often confused with _copy_ and _duplicate_. |
| **copy** | 🟠 Use with caution | Use when creating an exact copy in the same location as the original. Often confused with _clone_ and _duplicate_. |
| **could** | 🔴 Avoid | Replace with _can_ or _might_ whenever possible. |
| **create** | 🟢 Preferred | Use for creating an object from scratch Not _create new_.  _Delete_ is the correct opposite. |
| **delete** | 🟢 Preferred | Use when deleting data that users can no longer retrieve.  _Create_ is the correct opposite. |
| **disable** | 🟠 Use with caution | Don't use to describe something that is broken. Use _inactive_, _unavailable_, _deactivate_, _turn off_, or _deselect_, depending on the context.|
| **duplicate** | 🟠 Use with caution | Use when creating a copy of an object in the same location as the original.  Often confused with _copy_ and _clone_.  |
| **easy**, **easily** | 🔴 Avoid | It can be frustrating for users to think that something is easy, but then struggle to do the task. Typically the same meaning can be conveyed without this word.|
| **edit** | 🟢 Preferred | Not _change_ or _modify_. Edit is the better choice for localization. |
| **e.g.** | 🔴 Avoid | Don't use Latin abbreviations. Use _for example_ or _such as_ instead. |
| **enable** | 🟢 Preferred | Use when turning on or activating an option or a feature. |
| **enter** | 🟢 Preferred | Use to refer to the user entering text. Not _type_. |
| **execute** | 🔴 Avoid |Use _run_ or _start_ instead.|
| **hack** | 🔴 Avoid | For a noun, use _tip_ or _work-around_ instead. For a verb, use _configure_ or _modify_. |
| **hit** | 🔴 Avoid | For a noun, use _visits_ (as in web visits). For a verb, use _click_ or _press_.|
| **i.e.** | 🔴 Avoid | Don't use Latin abbreviations.|
| **invalid** | 🔴 Avoid | Use _not valid_ or _incorrect_ instead. |
| **kill** | 🟠 Use with caution | Use _cancel_ or _stop_ unless the actual command is `kill`. |
| **launch** | 🔴 Avoid | Use _open_ instead.  |
| **may** | 🟠 Use with caution | Use _may_ for permissibility. Use _can_ for capability. Use _might_ for possibility.  |
| **open** | 🟢 Preferred | Use instead of _launch_.  |
| **please** | 🔴 Avoid | In most cases, _please_ is unnecessary. Exceptions are situations where the user must wait or do something inconvenient. Or, if the text sounds too abrupt without it.  |
| **remove** | 🟢 Preferred | Use when removing a relationship, but not permanently deleting the data. For example, you remove a visualization from a dashboard. _Add_ is the correct opposite. |
| **select** | 🟢 Preferred | _Select_ is preferred over _choose_. |
| **simple**, **simply** | 🔴 Avoid | Often used before a before a verb like _select_, but doesn't add any information or value. Implies that users should have been able to do such a simple task without assistance.|
| **start** | 🟠 Use with caution | _Start_ and _begin_ depend on the context. _Start a program,_ _start an engine,_ or _start a timer_ are common phrases. Similarly, _begin a procedure,_ _begin an analysis,_ or _begin an installation_ are frequently used.  _Start_ is considered less formal than _begin_.|
| **terminate** | 🔴 Avoid | Use _stop_ or _exit_ instead.|
| **type** | 🔴 Avoid | Use _enter_ because there is typically more than one way to enter text than typing. |
| **unable** | 🟠 Use with caution | _Unable_ means not being able to perform an action. Often confused with cannot.  |
| **utilize** | 🟠 Use with caution | Don't use _utilize_ when you mean _use_. |
| **view** | 🟢 Preferred | Preferred over _see_ because _view_ is more inclusive. |
| **whitelist** | 🔴 Avoid | Use _allowlist_ instead. |