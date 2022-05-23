// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function printf(tpl: string, ...args: any[]): string {
    return tpl.replace(/%[sdf]/g, () => {
        const a = args.shift()
        if (a === undefined || a === null) {
            return ''
        }
        return a
    })
}
const errstr = {
    'A-01': 'Identifier %s started with a digit',
    'A-02': 'Unexpected character %s',
    'B-01': 'SyntaxError: %s',
    'C-01': '%s is larger than %s in array declaration',
    'C-02': 'Undefined variable %s',
    'C-03': 'Variable %s is already defined',
    'C-04': 'Cannot assign to %s (%s) with uncompatible type %s',
    'C-05': 'RECORD is uncomparable',
    'C-06': 'RECORD cannot be operated',
    'C-07': 'Undefined variable cannot be operated',
    'C-08': 'Undeclared operator %s %s',
    'C-09': 'Undefined variable cannot be used in expression',
    'C-10': 'Assigning from undefined variable %s',
    'C-11': 'Assigning to undefined variable %s',
    'C-12': 'Function got %s parameters, but expects %s',
    'C-13': 'Passing undefined variable to %s in function call',
    'C-14': 'Parameter %s got incompatible type %s, expected %s',
    'F-01': 'Uncompatible reference',
    'W-01': 'Assigning %s ( %s ) with type %s may lose precision',
    'W-02': 'Assigning parameter %s ( %s ) with type %s may lose precision',
} as Record<string, string>
export function errStr(code: string, value: string[]) {
    if (!errstr[code]) {
        return `${errstr[code]}: ${value.join(',')}`
    }
    return printf(errstr[code], ...(value || []))
}
