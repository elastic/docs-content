# Enrollment handling for containerized agents

For {{fleet}}-managed {{agents}} that run in a containerized environment (including Docker, Kubernetes, and others), enrollment handling is managed as follows:

* **Enrollment Verification:** {{agent}} checks the stored enrollment conditions within its container environment and re-enrolls only when necessary.
* **Unenrollment Handling:** If an {{agent}} is unenrolled through the {{fleet}} UI but still references a valid enrollment token provided through environment variables, it will automatically re-enroll on the next container restart.

In versions lower than 8.18, an unenrolled agent remains unenrolled and does not re-enroll, even if a valid enrollment token is still available.







