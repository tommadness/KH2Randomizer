mod = '''title: Randomizer Seed
assets:
- name: 00battle.bin
  method: binarc
  source:
  - name: fmlv
    method: listpatch
    type: List
    source:
      - name: FmlvList.yml
        type: fmlv
  - name: lvup
    method: listpatch
    type: List
    source:
      - name: LvupList.yml
        type: lvup
  - name: bons
    method: listpatch
    type: List
    source:
      - name: BonsList.yml
        type: bons
- name: 03system.bin
  method: binarc
  source:
  - name: trsr
    method: listpatch
    type: List
    source:
      - name: TrsrList.yml
        type: trsr
  - name: item
    method: listpatch
    type: List
    source:
      - name: ItemList.yml
        type: item    '''