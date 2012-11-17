Pyseudo Dx Features/Functions

Create company kirmse
    controllers.Cnt.CreateCmpKirmse

Relate kirmse to ni via Dx doc
    Create a relation between parent ni and child kirmse using a Dx doc.
        UI needs to provide selected OID for ni and kirmse.
        Assuming UI is focused on doc kirmse, user can choose to relate this doc to another doc OR add a child relationship.
            UI needs to provide the type relationship this is using a DxRel doc.
            Since kirmse is a Cmp class doc, UI presents a list of available DxRel titles/roles/association.
                For example: 
                    CompanyOf
                    DepartmentOf
                    BranchOf

    controllers.Dx.RelateKirmseToNi
        Pass in:
            toId: OID for ni
            frId: OID for kirmse
            dxRelId: OID for areaOf

        Process:
            Create dx
            Update kirmse
                Add ni as a parent/to of kirmse
                    Add a dRel to kirmse.tos
            Update ni
                Add kirmse a child/fr of ni
                    Add a dRel to ni.frs