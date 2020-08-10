<template>
    <el-card>
        <div style="margin-top: 20px; margin-bottom: 30px; text-align: center; font-size: 18px;">
            <span>老人微笑与交互事件</span>
        </div>
        <el-dialog
                title="事件图片"
                :visible.sync="showPic"
                width="550px"
                center>
            <el-image :src="picUrl">
                <div slot="placeholder" class="image-slot">
                    <div style="width: 500px; text-align: center">加载中...</div>
                </div>
                <div slot="error" class="image-slot">
                    <div style="width: 500px; text-align: center">加载失败</div>
                </div>
            </el-image>
            <span slot="footer" class="dialog-footer">
                <el-button @click="showPic = false">取 消</el-button>
                <el-button type="primary" @click="showPic = false">确 定</el-button>
            </span>
        </el-dialog>
        <el-table
                ref="filterTable"
                :data="eventData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase())).slice((currentPage-1)*listSize,currentPage*listSize)"
                stripe
                @row-dblclick="eventShow"
                style="width: 100%">
            <el-table-column
                    prop="ID"
                    label="ID"
                    width="80">
            </el-table-column>
            <el-table-column
                    prop="date"
                    label="日期"
                    sortable
                    width="180"
                    column-key="date"
                    :filters="dateMap"
                    :filter-method="filterHandler"
            >
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="老人姓名"
                    width="180">
            </el-table-column>
            <el-table-column
                    prop="address"
                    label="事件发生地点"
                    :formatter="formatter">
            </el-table-column>
            <el-table-column
                    prop="description"
                    label="事件描述">
            </el-table-column>
            <el-table-column>
                <template slot="header" slot-scope="scope">
                    <el-input
                            v-model="search"
                            size="mini"
                            placeholder="输入老人姓名搜索"/>
                </template>
            </el-table-column>
            <el-table-column
                    prop="tag"
                    label="事件"
                    width="100"
                    :filters="[{ text: '微笑', value: '微笑' }, { text: '交互', value: '交互' }]"
                    :filter-method="filterTag"
                    filter-placement="bottom-end">
                <template slot-scope="scope">
                    <el-tag
                            :type="scope.row.tag === '交互' ? 'success' : 'primary'"
                            disable-transitions>{{scope.row.tag}}
                    </el-tag>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-size="10"
                layout="total, prev, pager, next, jumper"
                :total="eventData.length">
        </el-pagination>
        <div style="margin-top: 20px; margin-right: 30px; margin-bottom: 50px; float: right;">
            <el-button type="success" round @click="resetDateFilter">清除日期过滤器</el-button>
            <el-button type="primary" round @click="clearFilter">清除所有过滤器</el-button>
        </div>
    </el-card>
</template>

<script>
    import API_PRO from "../../api/API_PRO";

    export default {
        name: "elderEventList",
        data() {
            return {
                search: '',
                eventData: [],
                imgURL: API_PRO.imageURL,
                picUrl: '',
                showPic: false,
                currentPage:1,
                listSize:10,
                dateMap: [],
            }
        },
        methods: {
            resetDateFilter() {
                this.$refs.filterTable.clearFilter('date');
            },
            clearFilter() {
                this.$refs.filterTable.clearFilter();
            },
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            filterHandler(value, row, column) {
                const property = column['property'];
                return row[property] === value;
            },
            handleCurrentChange(val) {
                this.currentPage = val;
            },
            setData(data) {
                this.eventData = data;
                for(let i=0; i<data.length; i++){
                    let pushFlag = true;
                    for(let j=0; j<this.dateMap.length; j++) {
                        if(this.dateMap[j].text === data[i].date){
                            pushFlag = false;
                            break;
                        }
                    }
                    if(pushFlag){
                        this.dateMap.push({text: data[i].date, value: data[i].date});
                    }
                }
            },
            eventShow(row, column, event) {
                for (let i = 0; i < this.eventData.length; i++) {
                    if (row.ID === this.eventData[i].ID) {
                        this.picUrl = this.imgURL + this.eventData[i].img_path;
                        this.showPic = true;
                        break;
                    }
                }
            },
        }
    }
</script>

<style scoped>

</style>
