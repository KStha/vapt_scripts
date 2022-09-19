# Contributing

## Issues

Please follow the following steps (in order) if you want to open issues:

1. Before opening an issue, make sure that you are using the latest version of the
   software, with latest changes, with all required dependancies.

2. If you are using the latest version of the software, with latest changes, and
   the issue is still present, before opening an issue, make sure that **same** or
   **similar** issue(s) are **not** opened already.

3. If same or similar issue(s) are not opened already, then, open issues with
   **clear reproducible steps**, providing as much detail as possible, which makes
   it easy for everyone to reproduce the issue, find problems, and solve them.

## Sign-off your commits and reverts

Every contributor **MUST** "sign-off" every contribution they make, either by
adding a `Signed-off-by` line manually (see 
[Sign-off Example](#sign-off-example)), or by using `git commit -s` for
commits, and `git revert -s` for reverts, which will add `Signed-off-by` line
automatically, to specify that they agree to the
[Developer Certificate of Origin](https://developercertificate.org/),
which is specified [below](#developer-certificate-of-origin), or at
[https://developercertificate.org/](https://developercertificate.org/).

### Developer Certificate of Origin

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

### Sign-off Example

A `Signed-off-by` line looks like this:

`Signed-off-by: Name Surname <local-part@domain>`

and should be added after the commit message (if description is NOT provided),
followed by a blank line, or AFTER description (if a description is provided),
followed by a blank line, as shown below:

```
<commit-message>

[description]

Signed-off-by: Name Surname <local-part@domain>
```
