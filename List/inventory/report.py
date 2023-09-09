from dataclasses import dataclass, field

from List.configDict import itemType
from List.inventory.item import InventoryItem


@dataclass(frozen=True)
class AnsemReport(InventoryItem):
    id: int
    name: str
    type: itemType = field(init=False, default=itemType.REPORT)
    report_number: int


AnsemReport1 = AnsemReport(226, "Secret Ansem's Report 1", report_number=1)
AnsemReport2 = AnsemReport(227, "Secret Ansem's Report 2", report_number=2)
AnsemReport3 = AnsemReport(228, "Secret Ansem's Report 3", report_number=3)
AnsemReport4 = AnsemReport(229, "Secret Ansem's Report 4", report_number=4)
AnsemReport5 = AnsemReport(230, "Secret Ansem's Report 5", report_number=5)
AnsemReport6 = AnsemReport(231, "Secret Ansem's Report 6", report_number=6)
AnsemReport7 = AnsemReport(232, "Secret Ansem's Report 7", report_number=7)
AnsemReport8 = AnsemReport(233, "Secret Ansem's Report 8", report_number=8)
AnsemReport9 = AnsemReport(234, "Secret Ansem's Report 9", report_number=9)
AnsemReport10 = AnsemReport(235, "Secret Ansem's Report 10", report_number=10)
AnsemReport11 = AnsemReport(236, "Secret Ansem's Report 11", report_number=11)
AnsemReport12 = AnsemReport(237, "Secret Ansem's Report 12", report_number=12)
AnsemReport13 = AnsemReport(238, "Secret Ansem's Report 13", report_number=13)


def all_reports() -> list[AnsemReport]:
    return [AnsemReport1, AnsemReport2, AnsemReport3, AnsemReport4, AnsemReport5, AnsemReport6, AnsemReport7,
            AnsemReport8, AnsemReport9, AnsemReport10, AnsemReport11, AnsemReport12, AnsemReport13]
