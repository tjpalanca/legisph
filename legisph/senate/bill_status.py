# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/02C-senate-bill_status.ipynb.

# %% auto 0
__all__ = ['PendingInCommittee', 'parse_senate_bill_status', 'JointProceedings', 'Introduced',
           'CommitteeReportCalendaredForOrdinaryBusiness', 'ConsolidatedOrSubstitutedInCommitteeReport',
           'TechnicalWorkingGroup', 'FirstReading', 'CommitteeProceedings', 'ApprovedOnSecondReading']

# %% ../../notebooks/02C-senate-bill_status.ipynb 1
import re
import datetime

from typing import List
from nbdev.showdoc import show_doc

from .models import SenateBill, Senator, SenateCommittee

# %% ../../notebooks/02C-senate-bill_status.ipynb 3
class PendingInCommittee(SenateBill.SenateBillStatus):
    name: str = "Pending in Committee"

    @classmethod
    def parse(cls, h):
        if h.item == "Pending in the Committee":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 7
def parse_senate_bill_status(
    status: SenateBill.SenateBillStatus,  # Senate Bill Status to parse into a subclass
    classes: list,  # List of classes through which to cycle
):
    actions = []
    for c in classes:
        action, cycle = c.parse(status)
        if action is not None:
            actions.append(action)
        if not cycle:
            break
    return actions


show_doc(parse_senate_bill_status)

# %% ../../notebooks/02C-senate-bill_status.ipynb 11
class JointProceedings(SenateBill.SenateBillStatus):
    name: str = "Conducted Joint Proceedings"

    @classmethod
    def parse(cls, h):
        if h.item == "Conducted JOINT COMMITTEE MEETINGS/HEARINGS;":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 14
class Introduced(SenateBill.SenateBillStatus):
    name: str = "Introduced by a Senator"
    senator: Senator

    @classmethod
    def parse(cls, h):
        if h.item.startswith("Introduced by Senator "):
            return (
                cls(
                    **h.dict(),
                    senator=Senator(
                        name=(
                            h.item.replace("Introduced by Senator ", "").replace(
                                ";", ""
                            )
                        )
                    )
                ),
                True,
            )
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 17
class CommitteeReportCalendaredForOrdinaryBusiness(SenateBill.SenateBillStatus):
    name: str = "Committe Report Calendared for Ordinary Business"

    @classmethod
    def parse(cls, h):
        if h.item == "Committee Report Calendared for Ordinary Business;":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 20
class ConsolidatedOrSubstitutedInCommitteeReport(SenateBill.SenateBillStatus):
    name: str = "Consolidated or Substituted in Committee Report"

    @classmethod
    def parse(cls, h):
        if h.item == "Consolidated/Substituted in the Committee Report":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 23
class TechnicalWorkingGroup(SenateBill.SenateBillStatus):
    name: str = "Conducted a Technical Working Group"

    @classmethod
    def parse(cls, h):
        if h.item == "Conducted TECHNICAL WORKING GROUP;":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 26
class FirstReading(SenateBill.SenateBillStatus):
    name: str = "Read on First Reading and Referred to Committee"
    committees: List[SenateCommittee]

    @classmethod
    def parse(cls, h):
        slug1 = "Read on First Reading and Referred to the Committee on "
        slug2 = "Read on First Reading and Referred to the Committee(s) on "
        if h.item.startswith(slug1):
            committee = SenateCommittee(name=h.item.replace(slug1, "").replace(";", ""))
            return (cls(**h.dict(), committees=[committee]), False)
        if h.item.startswith(slug2):
            committees = h.item.replace(slug2, "")
            committees = re.split("[ ]*and[ ]*|[ ]*;[ ]*", committees)
            committees = [
                SenateCommittee(name=name) for name in committees if name != ""
            ]
            return (cls(**h.dict(), committees=committees), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 31
class CommitteeProceedings(SenateBill.SenateBillStatus):
    name: str = "Conducted Committee Proceedings"

    @classmethod
    def parse(cls, h):
        if h.item == "Conducted COMMITTEE MEETINGS/HEARINGS;":
            return (cls(**h.dict()), False)
        return (None, True)

# %% ../../notebooks/02C-senate-bill_status.ipynb 34
class ApprovedOnSecondReading(SenateBill.SenateBillStatus):
    name: str = "Approved On Second Reading"
    with_amendments: bool

    @classmethod
    def parse(cls, h):
        if h.item == "Approved on Second Reading with Amendments;":
            return (cls(**h.dict(), with_amendments=True), False)
        if h.item == "Approved on Second Reading without Amendment;":
            return (cls(**h.dict(), with_amendments=False), False)
        return (None, True)
