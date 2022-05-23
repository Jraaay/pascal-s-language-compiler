<template>
    <div class="c-container">
        <el-row class="c-header">
            <el-col :span="12">
                <div class="left title">Pas2C GUI</div>
                <div class="right">
                    <el-select class="precode" placeholder="加载预置代码" @change="codeSrc = $event.trim()">
                        <el-option
                            v-for="i in precode"
                            :key="i.file_name"
                            :label="i.file_name"
                            :value="i.code"
                        ></el-option>
                    </el-select>
                    <button class="run-btn" :disabled="loading" @click="apiCompile">
                        <i :class="loading ? 'codicon codicon-refresh' : 'codicon codicon-play'"></i>
                    </button>
                </div>
            </el-col>
            <el-col :span="12">
                <el-tabs v-model="currentTab" type="card" stretch>
                    <el-tab-pane label="编译结果" name="output"></el-tab-pane>
                    <el-tab-pane name="err">
                        <template #label>
                            <el-badge
                                class="errbdg"
                                :class="{ warning: results.error.length <= 0 }"
                                :value="computedErrors.length"
                                :hidden="computedErrors.length <= 0"
                            >
                                <span>错误和警告</span>
                            </el-badge>
                        </template>
                    </el-tab-pane>
                    <el-tab-pane label="语法树" name="ast"></el-tab-pane>
                    <el-tab-pane label="符号表" name="sym"></el-tab-pane> </el-tabs
            ></el-col>
        </el-row>
        <el-row class="c-content">
            <el-col :span="12">
                <MonacoEditor
                    ref="srcEditor"
                    class="c-editor ed-left"
                    theme="vs-dark"
                    language="pascal"
                    :value="codeSrc"
                    :options="{
                        DefaultEndOfLine: 1,
                        EndOfLinePreference: 1,
                    }"
                    @change="editorChange"
                    @editor-will-mount="editorWillMount"
            /></el-col>
            <el-col :span="12" style="border-left: 1px solid #444444">
                <div ref="treeCon" style="height: 100%">
                    <div v-show="currentTab === 'output'" class="ed-right-container">
                        <MonacoEditor
                            ref="dstEditor"
                            class="c-editor ed-right"
                            theme="vs-dark"
                            language="c"
                            :value="results.code"
                            :options="{ readOnly: true }"
                        />
                    </div>
                    <div v-show="currentTab === 'err'" class="c-right">
                        <el-scrollbar :height="(treeConHeight || 300) - 1">
                            <el-empty
                                v-show="computedErrors.length <= 0"
                                description="0 Error(s), 0 Warning(s)"
                            ></el-empty>
                            <div v-for="(i, a) in computedErrors" :key="a" class="erritem">
                                <div class="left">
                                    <i
                                        class="codicon"
                                        :class="i.code.includes('W') ? 'codicon-warning' : 'codicon-error'"
                                    ></i>
                                </div>
                                <div class="right">
                                    <div class="message">
                                        {{ i.message }}
                                    </div>
                                    <div class="bottom">
                                        <div class="code">{{ i.code }}</div>
                                        <div class="line">Line {{ i.line }}, Col {{ i.column }}</div>
                                    </div>
                                </div>
                            </div>
                        </el-scrollbar>
                    </div>
                    <div v-show="currentTab === 'ast'" class="c-right">
                        <el-scrollbar :height="(treeConHeight || 300) - 1">
                            <div style="height: 20px"></div>
                            <el-tree
                                node-key="id"
                                :data="computedAstData.tree"
                                :default-expanded-keys="computedAstData.expanded"
                            >
                                <template #default="{ data }">
                                    <span class="el-tree-node__label">
                                        <span v-if="data.children">
                                            <span class="key object">{{ data.label }}</span>
                                        </span>
                                        <span v-else>
                                            <span class="key">{{ data.key }}</span>
                                            <span class="value jstype" :class="String(typeof data.value)">{{
                                                data.value
                                            }}</span>
                                        </span>
                                    </span>
                                </template>
                            </el-tree>
                        </el-scrollbar>
                    </div>
                    <div v-show="currentTab === 'sym'" class="c-right">
                        <el-scrollbar :height="(treeConHeight || 300) - 1">
                            <div style="height: 20px"></div>
                            <el-tree
                                node-key="id"
                                :data="computedSymTree.tree"
                                :default-expanded-keys="computedSymTree.expanded"
                                :indent="30"
                            >
                                <template #default="{ data }">
                                    <span class="el-tree-node__label">
                                        <span v-if="data.value">
                                            <!--常量-->
                                            <span class="symtype" :class="data.type.toLowerCase()">
                                                {{ data.type }}
                                            </span>
                                            <span class="key symkey">
                                                {{ data.token }}
                                            </span>
                                            <span class="value jstype" :class="String(typeof data.value.value)">
                                                {{ data.value.value }}
                                            </span>
                                        </span>
                                        <span v-else-if="typeof data.isArray === 'boolean'">
                                            <!--变量-->
                                            <span class="symtype" :class="data.type.toLowerCase()">
                                                {{ data.type }}
                                            </span>
                                            <span class="key symvar" :class="data.children ? 'object' : ''">
                                                {{
                                                    typeof data.token === 'string'
                                                        ? data.token
                                                        : data.token.ids.join('.')
                                                }}<span v-if="data.isArray">
                                                    <span v-for="(i, a) in data.size" :key="a">
                                                        <span style="color: #fff">[</span>
                                                        <span class="jstype number">{{ i }}</span>
                                                        <span style="color: #fff">]</span>
                                                    </span>
                                                </span>
                                            </span>
                                            <span v-if="data.isArray" class="value">
                                                start=<span v-for="(i, a) in data.start" :key="a">
                                                    <span style="color: #fff">[</span>
                                                    <span class="jstype number">{{ i }}</span>
                                                    <span style="color: #fff">]</span>
                                                </span>
                                            </span>
                                        </span>
                                        <span v-else-if="data.table">
                                            <span class="symtype" :class="data.type ? data.type.toLowerCase() : 'void'">
                                                {{ data.type || 'VOID' }}
                                            </span>
                                            <span class="key object">
                                                {{ data.token }}(<span v-for="i in data.table.params" :key="i">
                                                    <span
                                                        class="symtype functype"
                                                        :class="data.table.variables[i - 1].type.toLowerCase()"
                                                    >
                                                        {{ data.table.variables[i - 1].type }}
                                                    </span>
                                                    <span v-if="data.table.references[i - 1]" class="funcref">&</span>
                                                    <span class="jstype variable">{{
                                                        data.table.variables[i - 1].token
                                                    }}</span>
                                                    <span v-if="i < data.table.params" style="color: #fff"
                                                        >,
                                                    </span> </span
                                                >)
                                            </span>
                                        </span>
                                        <span v-else>
                                            <i v-if="data.icon" class="symicon" :class="data.icon"></i>
                                            {{ data.label }}
                                        </span>
                                    </span>
                                </template>
                            </el-tree>
                        </el-scrollbar>
                    </div>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { MarkerSeverity } from 'monaco-editor'
import { errStr } from './errors'
import { ISymbolTable, IErrorData } from './typing'
import { useElementSize, useEventListener, useDebounceFn } from '@vueuse/core'
import { defineComponent, computed, ref, h, watch, nextTick } from 'vue'
import MonacoEditor from 'vue-monaco'
import { ElNotification } from 'element-plus'
MonacoEditor.render = () => h('section')
export default defineComponent({
    name: 'App',
    components: { MonacoEditor },
    setup() {
        const loading = ref(false)
        const currentTab = ref('output')
        const codeSrc = ref(``)
        const results = ref({
            srcCode: ``,
            code: ``,
            ast: {},
            symbolTable: {},
            error: [] as IErrorData[],
            warning: [] as IErrorData[],
        })
        const srcEditor = ref(null as any)
        const dstEditor = ref(null as any)
        const editorChange = (ev: unknown) => {
            if (typeof ev === 'string') {
                codeSrc.value = ev
            }
        }
        watch(codeSrc, async () => {
            await nextTick()
            await nextTick()
            if (srcEditor.value) {
                srcEditor.value.getEditor().getModel().setEOL(1)
            }
        })
        const debouncedEditorResize = useDebounceFn(() => {
            if (srcEditor.value) {
                srcEditor.value.getEditor().layout()
            }
            if (dstEditor.value) {
                dstEditor.value.getEditor().layout()
            }
        }, 100)
        useEventListener('resize', debouncedEditorResize, { passive: true })
        let monaco: any = null
        const editorWillMount = (m: any) => {
            monaco = m
        }
        const objectToElTree = (obj: any, id = { id: 0 }): any => {
            const elTree = []
            for (const key in obj) {
                if (Object.prototype.hasOwnProperty.call(obj, key)) {
                    const value = obj[key]
                    if (typeof value === 'object') {
                        elTree.push({
                            id: id.id++,
                            label: key,
                            children: objectToElTree(value, id),
                        })
                    } else {
                        elTree.push({
                            id: id.id++,
                            label: `${key}: ${value}`,
                            key: key,
                            value: value,
                        })
                    }
                }
            }
            return elTree
        }
        const computedAstData = computed(() => {
            const id = { id: 0 }
            const tree = objectToElTree(results.value.ast, id)
            const expanded = []
            for (const i of tree) {
                expanded.push(i.id)
                if (!i.children) continue
                for (const j of i.children) {
                    expanded.push(j.id)
                }
            }
            return {
                tree,
                expanded,
            }
        })
        const getSymTreeArray = (obj: ISymbolTable, id = { id: 0 }): any => {
            const elTree = []
            if (obj.constants) {
                elTree.push({
                    id: 'constant-' + id,
                    label: '全局常量',
                    icon: 'codicon codicon-symbol-constant',
                    children: obj.constants,
                })
            }
            if (obj.variables) {
                const v = obj.variables.map((e) => {
                    if (e.recordTable) {
                        id.id++
                        const c = getSymTreeArray(e.recordTable, id)
                        return {
                            ...e,
                            children: c[0].children,
                        }
                    }
                    return e
                })
                elTree.push({
                    id: 'variable-' + id,
                    label: '全局变量',
                    icon: 'codicon codicon-symbol-variable',
                    children: v,
                })
            }
            if (obj.subFunc) {
                const v = obj.subFunc.map((e) => {
                    if (e.table) {
                        id.id++
                        const c = getSymTreeArray(
                            {
                                constants: e.table.constants,
                                variables: e.table.variables?.slice((e.table as typeof e).params),
                            },
                            id,
                        )
                        c.forEach((e: any) => {
                            e.label = e.label.replace('全局', '局部')
                        })
                        return {
                            ...e,
                            children: c,
                        }
                    }
                    return e
                })
                elTree.push({
                    id: 'subfunc-' + id,
                    label: '函数',
                    icon: 'codicon codicon-symbol-function',
                    children: v,
                })
            }
            return elTree
        }
        const computedSymTree = computed(() => {
            const id = { id: 0 }
            const tree = getSymTreeArray(results.value.symbolTable as ISymbolTable, id)
            const expanded = []
            for (const i of tree) {
                expanded.push(i.id)
                if (!i.children) continue
                for (const j of i.children) {
                    expanded.push(j.id)
                }
            }
            return {
                tree,
                expanded,
            }
        })
        const calcColumn = (code: string, lexpos: number): number => {
            let col = 0
            for (let i = 0; i < lexpos; i++) {
                if (code[i] === '\n') {
                    col = 0
                } else {
                    col++
                }
            }
            return col
        }
        const computedErrors = computed(() => {
            // 获取开头空行的数量
            const lines = results.value.srcCode.split('\n')
            let empty = 0
            for (const i of lines) {
                if (i.trim() === '') {
                    empty++
                } else {
                    break
                }
            }

            return [...results.value.error, ...results.value.warning].map((e) => {
                return {
                    code: e.code,
                    line: e.info.line + empty,
                    column: calcColumn(results.value.srcCode.trim(), e.info.lexpos),
                    end_column: e.info.end_lexpos
                        ? calcColumn(results.value.srcCode.trim(), e.info.end_lexpos)
                        : undefined,
                    message: errStr(e.code, e.info.value),
                }
            })
        })
        const computedMarkers = computed(() => {
            const srcLine = codeSrc.value.split('\n')
            const dstLine = results.value.srcCode.split('\n')
            if (srcLine.length !== dstLine.length) {
                return []
            }
            return computedErrors.value.map((e) => {
                const line = dstLine[e.line - 1]
                const sline = srcLine[e.line - 1]
                if (!line || line.trim() !== sline.trim()) return {}
                const firstNonSpaceIndex = line.search(/\S/)
                return {
                    startLineNumber: e.line,
                    startColumn: (e.column || firstNonSpaceIndex) + 1,
                    endLineNumber: e.line,
                    endColumn: e.end_column ? e.end_column : line.length + 1,
                    severity: e.code.includes('W') ? MarkerSeverity.Warning : MarkerSeverity.Error,
                    message: e.message,
                    code: e.code,
                }
            })
        })

        watch([computedMarkers, srcEditor], () => {
            if (!srcEditor.value || !monaco) return
            monaco.editor.setModelMarkers(srcEditor.value.getEditor().getModel(), 'pas2c', computedMarkers.value)
        })
        const toJsType = (type: string) => {
            switch (type) {
                case 'integer':
                case 'real':
                    return 'number'
                case 'char':
                    return 'string'
                case 'boolean':
                    return 'boolean'
                case 'record':
                    return 'object'
            }
            return type
        }
        async function apiCompile() {
            if (loading.value) return
            loading.value = true
            codeSrc.value = codeSrc.value.trim()
            const s = codeSrc.value
            try {
                const res = await fetch('/api', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'text/plain',
                    },
                    body: s,
                })
                if (!res.ok) {
                    throw new Error(`${res.status} ${res.statusText}`)
                }
                const data = await res.json()
                data.srcCode = s
                results.value = data
                if (data.error.length > 0) {
                    currentTab.value = 'err'
                } else {
                    currentTab.value = 'output'
                }
            } catch (e) {
                ElNotification.error({
                    title: '出错了！',
                    message: (e as Error).message,
                })
            }
            loading.value = false
        }
        const precode = ref([] as { file_name: string; code: string }[])
        fetch('/api').then(async (res) => {
            if (!res.ok) {
                ElNotification.error({
                    title: '获取预置代码失败',
                    message: `${res.status} ${res.statusText}`,
                })
                return
            }
            const data = await res.json()
            precode.value = data
            precode.value = precode.value.sort((a, b) => {
                return a.file_name.localeCompare(b.file_name)
            })
        })
        const treeCon = ref(null as null | HTMLDivElement)
        const { height: treeConHeight } = useElementSize(treeCon)
        return {
            codeSrc,
            results,
            editorChange,
            editorWillMount,
            currentTab,
            computedAstData,
            treeCon,
            treeConHeight,
            computedSymTree,
            toJsType,
            computedErrors,
            loading,
            apiCompile,
            precode,
            srcEditor,
            dstEditor,
        }
    },
})
</script>

<style lang="scss">
HTML,
body,
#app,
.c-container,
.ed-right-container {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}
.c-editor {
    width: 100%;
    height: 100%;
}
.c-container {
    display: flex;
    flex-direction: column;
    background: #323233;
}

.c-header {
    flex-basis: 40px;
    min-height: 40px;
    max-height: 40px;
    overflow: hidden;
    .right {
        padding: 0 16px;
        float: right;
        height: 40px;
        display: flex;
        align-items: center;
        background: #252526;
    }

    .run-btn {
        appearance: none;
        background: transparent;
        border: 0;
        height: 32px;
        width: 32px;
        cursor: pointer;
        transition: all 0.2s;
        i {
            font-size: 20px !important;
        }
        &:hover {
            background: #323233;
        }
        &[disabled] {
            cursor: not-allowed;
            &:hover {
                background: transparent;
            }
        }
    }
    .precode {
        width: 130px;
        margin-right: 15px;
    }
}

.c-content {
    flex: 1;
}
.c-right {
    background: #1e1e1e;
    height: 100%;
    box-sizing: border-box;
}
.el-tabs--card > .el-tabs__header .el-tabs__item {
    border: 0 !important;
}

.el-tabs--card > .el-tabs__header .el-tabs__item.is-active {
    background: #1e1e1e;
    color: var(--el-text-color-primary);
    box-shadow: 0px 0px 1px #000;
}
.errbdg sup {
    transform: translateY(-5%) translateX(125%) !important;
}
.errbdg.warning sup {
    background: var(--el-color-warning);
}
.el-tree-node__label .key {
    padding: 0 5px;
    color: #98dcf0;
    font-size: 14px;
    display: inline-block;
    height: 22px;
    box-sizing: border-box;
    line-height: 22px;
    margin-right: 3px;
    font-family: Consolas, monospace;
    vertical-align: middle;
    &::after {
        content: ':';
    }
    &.symkey::after {
        content: '=';
        color: #fff;
        padding-left: 5px;
    }
    &.symvar::after {
        content: '';
    }
}

.el-tree-node__label .value {
    display: inline-block;
    vertical-align: middle;
    color: #d09177;
    background: rgba(255, 255, 255, 0.1);
    padding: 1px 5px;
    font-size: 14px;
    height: 22px;
    font-family: Consolas, monospace;
    line-height: 22px;
}

.jstype.variable {
    color: #98dcf0;
}
.jstype.number {
    color: #b5cea8;
}
.jstype.object {
    color: #dddcaa;
}
.jstype.string {
    color: #d09177;
}

.el-tree-node__label .key.object {
    color: #dddcaa;
    &::after {
        content: '';
    }
}

.symtype {
    height: 22px;
    font-size: 12px;
    display: inline-block;
    line-height: 22px;
    vertical-align: middle;
    background: #555;
    margin-right: 5px;
    width: 60px;
    box-sizing: border-box;
    text-align: center;
    border-radius: 2px;
    font-family: Consolas, monospace;
}

.symtype.integer,
.symtype.real {
    background: #4e8e2f;
}

.symtype.char {
    background: #a77730;
}
.symtype.record {
    background: #3375b9;
}
.symtype.functype {
    width: auto;
    padding: 0 2px;
    height: 16px;
    line-height: 16px;
    margin-bottom: 2px;
    margin-right: 2px;
}
.funcref {
    color: #f56c6c;
}
.symicon {
    position: relative;
    top: 2px;
}
.erritem {
    display: flex;
    color: var(--el-text-color-primary);
    font-size: 13px;
    padding: 10px 5px;
    border-bottom: 1px solid #393939;
    .right {
        flex: 1;
        padding-right: 10px;
    }
    .left {
        flex-basis: 40px;
        i {
            font-size: 20px;
            display: flex;
            align-content: center;
            justify-content: center;
            height: 100%;
            padding-top: 5px;
            color: #e6a23c;
            &.codicon-error {
                color: #f56c6c;
            }
        }
    }

    .bottom {
        opacity: 0.7;
        .code {
            float: left;
        }
        .line {
            float: right;
            font-size: 12px;
        }
    }
}
.editor-widget.suggest-widget {
    display: none;
}
@keyframes rotate {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
.codicon-refresh {
    animation: rotate 1s linear infinite;
}
</style>
<style lang="scss" scoped>
.left.title {
    float: left;
    height: 40px;
    padding: 9px 15px;
    color: #fff;
    box-sizing: border-box;
}
</style>
