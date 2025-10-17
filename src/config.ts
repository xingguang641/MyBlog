import type {
	ExpressiveCodeConfig,
	LicenseConfig,
	NavBarConfig,
	ProfileConfig,
	SiteConfig,
} from "./types/config";
import { LinkPreset } from "./types/config";

export const siteConfig: SiteConfig = {
	title: "星光",
	subtitle: "深度学习知识分享网站",
	lang: "zh_CN", // 语言代码，例如 'en'、'zh_CN'、'ja' 等
	themeColor: {
		hue: 250, // 主题颜色的默认色相，取值范围 0~360，例如红色:0，青绿色:200，蓝绿色:250，粉色:345
		fixed: false, // 隐藏访客的主题颜色选择器
	},
	banner: {
		enable: true,
		src: "assets/images/demo-banner.png", // 相对于 /src 目录的路径。如果以 '/' 开头则是相对于 /public 目录
		position: "center", // 等同于 CSS 的 object-position，仅支持 'top'、'center'、'bottom'，默认是 'center'
		credit: {
			enable: false, // 是否显示横幅图片的署名文字
			text: "", // 要显示的署名文字
			url: "", // （可选）原作者或作品页面的链接
		},
	},
	toc: {
		enable: true, // 在文章右侧显示目录
		depth: 2, // 目录中显示的最大标题层级，范围 1~3
	},
	favicon: [
		{
			src: "/favicon/favicon.png"
		},
	],
};

export const navBarConfig: NavBarConfig = {
	links: [LinkPreset.Home, LinkPreset.Archive, LinkPreset.About],
};

export const profileConfig: ProfileConfig = {
	avatar: "assets/images/avatar1.jpg", // 相对于 /src 目录的路径。如果以 '/' 开头则是相对于 /public 目录
	name: "星光",
	bio: "学无止境 探索未知",
	links: [
		{
			name: "Bilibili",
			icon: "simple-icons:bilibili", // 图标代码可在 https://icones.js.org/ 查询
			// 如果尚未包含对应的图标集，需要手动安装
			// `pnpm add @iconify-json/<icon-set-name>`
			url: "https://space.bilibili.com/471173444",
		},
		{
			name: "Yuque",
			icon: "fa6-brands:twitter", // 临时用 Twitter 图标替代
			url: "https://www.yuque.com/xiaoxiesheng/ubc4e3",
		},
		{
			name: "GitHub",
			icon: "fa6-brands:github",
			url: "https://github.com/xingguang641",
		},
	],
};

export const licenseConfig: LicenseConfig = {
	enable: true,
	name: "CC BY-NC-SA 4.0",
	url: "https://creativecommons.org/licenses/by-nc-sa/4.0/",
};

export const expressiveCodeConfig: ExpressiveCodeConfig = {
	// 注意：部分样式（例如背景颜色）在 astro.config.mjs 文件中被覆盖
	// 请务必选择深色主题，因为此博客主题目前只支持深色背景
	theme: "github-dark",
};
