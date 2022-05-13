export interface IErrorData {
    code: string
    info: {
        line: number
        lexpos: number
        value: string[]
        end_lexpos?: number
    }
}
export type ISymbolType = 'INTEGER' | 'REAL' | 'BOOLEAN' | 'RECORD' | 'CHAR'
export interface ISymbolTableConst {
    id: number
    token: string
    type: ISymbolType
    value: {
        length: string
        type: string
        _type: string
        value: string | number | boolean
    }
    positive: true
}
export interface ISymbolTableVar {
    id: number
    token:
        | string
        | {
              type: string
              ids: string[]
          }
    type: ISymbolType
    isArray: boolean
    dimension: number
    size: number[]
    start: number[]
    recordTable: null | {
        variables: ISymbolTableVar[]
    }
}
export interface ISymbolTablFunc {
    id: number
    token: string
    type: ISymbolType
    // eslint-disable-next-line no-use-before-define
    table: ISymbolTable
    params: number
    references: boolean[]
}
export interface ISymbolTable {
    constants?: ISymbolTableConst[]
    variables?: ISymbolTableVar[]
    subFunc?: ISymbolTablFunc[]
}
