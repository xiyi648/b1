// 页面加载完成后执行
window.onload = function() {
    // 简单加载提示
    console.log("b1.qklm.xyz 页面资源加载完成");
    
    // 给按钮/元素添加交互（若 index.html 有按钮可绑定）
    const heading = document.querySelector('h1');
    if (heading) {
        heading.addEventListener('click', function() {
            alert('你点击了标题！这是一个简单交互示例～');
        });
    }
};