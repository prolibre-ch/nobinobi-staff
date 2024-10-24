.. :changelog:

History
-------

0.1.6.12 (2024-10-18)
++++++++++++++++++++++
* Fix bug python version

0.1.6.11 (2024-10-18)
++++++++++++++++++++++
* 2ccf3de - Add bump2version to dev requirements
* 986ce77 - ignore DB
* bcead03 - Fix requirements
* 53d8592 - Fix bug with django-admin-rangefilter
* Update requirements

0.1.6.10 (2023-06-19)
++++++++++++++++++++++

* Update requirements

0.1.6.9 (2023-06-14)
++++++++++++++++++++++

* Update requirements

0.1.6.8 (2021-12-23)
++++++++++++++++++++++

* 879490a - filter on choice staff absence only active staff
* d04ba24 - Fix bug when save staff for training

0.1.6.7 (2021-12-22)
++++++++++++++++++++++

* c19f6cb - Filter by default to staff active in list admin
* dd97bda - Fix requirements

0.1.6.6 (2021-12-14)
++++++++++++++++++++++

* 7562c55 - Change str format in full name by last_name - first_name
* 78bf3e3 - Fix error import
* Update requirements

0.1.6.5.2 (2021-09-29)
++++++++++++++++++++++

* 022c118 - Fix import missing in commands
* Update requirements

0.1.6.5.1 (2021-09-17)
++++++++++++++++++++++

* 002cb4c - fix bug with search field icontains

0.1.6.5 (2021-09-17)
+++++++++++++++++++++

* c4dd7a1 - Add search field for training
* 3a28df3 - Fix error with generate command when staffs args filled

0.1.6.4 (2021-09-17)
+++++++++++++++++++++

* 7599706 - Update traduction
* 0581582 - Update system to generate and update training auto
* a60c325 - Add default_auto_field

0.1.6.3 (2021-09-16)
+++++++++++++++++++++

* 4d973ec - Update "update command" for training
* 184406d - Change signals to update training when absence
* 88245dd - Change admin display in training add select related in staff
* 2a0b8f8 - Add method to get datetime_range in model add tracker in absence to get previous date

0.1.6.2 (2021-09-14)
+++++++++++++++++++++

* Update requirements.
* 2fb2bfa - Add signal when absence is saved and training not created

0.1.6.1 (2021-06-07)
+++++++++++++++++++++

* Update requirements.
* Update django for security fix

0.1.6 (2021-04-13)
++++++++++++++++++++

* 186a796 - Fix upload publish
* Update requirements.

0.1.5 (2021-03-12)
++++++++++++++++++++

* Add an export function for Absence
* Update requirements.
* Update traduction FR.

0.1.4 (2020-10-29)
++++++++++++++++++++

* Add fields ["picture", "nationality", "civil_status", "status", "status_modified", "created", "modified"].
* Rename field "avs" to "social_security_number".
* Rename field "active" to "active_status".
* Add method to archive staff when select in admin staff list.
* Update search_field, list_display, list_filter fields.
* Remove load absence_type auto, now you have to load data.
* Update traduction FR.

0.1.3.1 (2020-09-08)
++++++++++++++++++++

* Update for staff

0.1.3 (2020-08-28)
++++++++++++++++++

* Update

0.1.0 (2020-08-20)
++++++++++++++++++

* First release on PyPI.
